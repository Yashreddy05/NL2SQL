"""
vanna_setup.py
──────────────
Final working Vanna 2.0 Agent setup (fixed).
"""

import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "clinic.db"

# ── Schema ────────────────────────────────────────────────────────────────────
SCHEMA_DDL = """
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    department TEXT,
    phone TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
);
"""

# ── STRONG SYSTEM PROMPT (forces SQL usage) ────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an AI SQL agent.\n\n"

    "STRICT RULES:\n"
    "- ALWAYS use the run_sql tool\n"
    "- NEVER answer in plain text\n"
    "- ALWAYS generate SQL\n"
    "- ONLY SELECT queries allowed\n"
    "- DO NOT explain anything\n"
    "- RETURN ONLY tool output\n\n"

    "DATABASE SCHEMA:\n"
    + SCHEMA_DDL
)

# ── Agent Factory ─────────────────────────────────────────────────────────────
def create_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")

    from vanna import Agent, AgentConfig
    from vanna.core.registry import ToolRegistry
    from vanna.core.user import UserResolver, User, RequestContext
    from vanna.tools import RunSqlTool, VisualizeDataTool
    from vanna.tools.agent_memory import (
        SaveQuestionToolArgsTool,
        SearchSavedCorrectToolUsesTool,
    )
    from vanna.integrations.sqlite import SqliteRunner
    from vanna.integrations.local.agent_memory import DemoAgentMemory
    from vanna.integrations.google import GeminiLlmService
    from vanna.core.system_prompt.default import DefaultSystemPromptBuilder

    # ── LLM ───────────────────────────────────────────────────────────────────
    llm_service = GeminiLlmService(
        api_key=api_key,
        model="gemini-2.5-flash",
        temperature=0.3,
    )
    print("[1/6] LLM ready")

    # ── DB Runner ─────────────────────────────────────────────────────────────
    sql_runner = SqliteRunner(database_path=DB_PATH)
    print("[2/6] DB ready")

    # ── Memory ────────────────────────────────────────────────────────────────
    memory = DemoAgentMemory(max_items=10000)
    print("[3/6] Memory ready")

    # ── Tools ────────────────────────────────────────────────────────────────
    registry = ToolRegistry()

    registry.register_local_tool(
        RunSqlTool(sql_runner=sql_runner),
        access_groups=["default"]
    )

    registry.register_local_tool(
        VisualizeDataTool(),
        access_groups=["default"]
    )

    registry.register_local_tool(
        SaveQuestionToolArgsTool(),
        access_groups=["default"]
    )

    registry.register_local_tool(
        SearchSavedCorrectToolUsesTool(),
        access_groups=["default"]
    )

    print("[4/6] Tools ready")

    # ── User Resolver ────────────────────────────────────────────────────────
    class DefaultUserResolver(UserResolver):
        async def resolve_user(self, context) -> User:
            return User(id="default_user", name="Clinic User")

    user_resolver = DefaultUserResolver()
    print("[5/6] User ready")

    # ── FIXED PROMPT BUILDER (NO FAIL CASE) ───────────────────────────────────
    class ClinicPromptBuilder(DefaultSystemPromptBuilder):
        def build(self, context=None):
            base = super().build(context)
            return SYSTEM_PROMPT + "\n\n" + (base or "")

    # ── Agent Config ─────────────────────────────────────────────────────────
    config = AgentConfig(
        temperature=0.3,
        max_tool_iterations=10,
        stream_responses=False
    )

    # ── Agent ────────────────────────────────────────────────────────────────
    agent = Agent(
        llm_service=llm_service,
        tool_registry=registry,
        user_resolver=user_resolver,
        agent_memory=memory,
        config=config,
        system_prompt_builder=ClinicPromptBuilder(),   # ✅ FIXED
    )

    print("[6/6] Agent ready")
    return agent


# ── Export ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Creating agent...")
    a = create_agent()
    print("Agent created successfully!")

else:
    print("Initializing agent...")
    agent = create_agent()
    memory = agent.agent_memory
    print("Agent ready!")
