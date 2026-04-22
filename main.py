import re
import sqlite3
import logging
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from vanna_setup import agent, DB_PATH, SCHEMA_DDL

# ── Logging ─────────────────────────────
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# ── App ────────────────────────────────
app = FastAPI(title="Clinic NL2SQL API")   # initializes the API service using FASTAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
) #this allows frontend applications to access the api

# ── SQL validation ─────────────────────
BLOCKED = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\b", re.I) # to prevent harmful queries ,i restrict only select  statements  and block destructive SQL commands

def validate_sql(sql: str):
    if not sql.upper().startswith("SELECT"):
        return False
    if BLOCKED.search(sql):
        return False
    return True


# ── Models ─────────────────────────────
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3) # defines input schema using pydantic 


class ChatResponse(BaseModel):
    message: str
    sql_query: Optional[str] = None
    columns: Optional[list[str]] = None
    rows: Optional[list[list[Any]]] = None
    row_count: Optional[int] = None


# ── DB helper ──────────────────────────
def run_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return rows, columns
 # Executes  SQL query on SQLite database returns rows and columns names

# ── /chat ──────────────────────────────
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    question = req.question.strip() #user input 
    log.info("Question: %s", question)

    from vanna.core.user import RequestContext
    context = RequestContext(user_id="default")

    result = None

    # 🔹 Try agent first
    try:
        async for chunk in agent.send_message(
            message=question,
            request_context=context
        ):
            result = chunk

        print("AGENT RESULT:", result)

    except Exception as e:
        log.error("Agent failed: %s", e)

    # 🔥 If agent failed → FORCE SQL
    sql = None

    if isinstance(result, dict):
        sql = result.get("sql")

    if not sql: # if the agent fails i implemented a fallback mechanism  using gemini API directly to ensure robustness 
        log.warning("⚠️ Using fallback SQL generation")
        import google.generativeai as genai
        import os
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model=genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Convert this question to SQL:

        {question}

        Schema:
        {SCHEMA_DDL}

        Only return SQL.
        """

        response = model.generate_content(prompt)
        sql= response.text.strip()
        #clear markdown
        sql = sql.replace("```sql", "").replace("```", "").strip()

        print("Generated SQL:", sql)

    # ── Validate SQL
    if not validate_sql(sql): #ensures only safe queries are executed
        return ChatResponse(
            message="Invalid SQL generated",
            sql_query=sql
        )
    if not sql:
        raise HTTPException(status_code=500, detail="SQL generation failed")
    # ── Execute SQL
    try:
        rows, columns = run_sql(sql) #execute sql
    except Exception as e:
        return ChatResponse(
            message=f"SQL execution failed: {e}",
            sql_query=sql
        ) # returns SQL,data and metadata like row count

    return ChatResponse(
        message="Success",
        sql_query=sql,
        columns=columns,
        rows=rows,
        row_count=len(rows)
    )


# ── health ─────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ── root ───────────────────────────────
@app.get("/")
def root():
    return {"msg": "API running"}

