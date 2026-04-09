# Clinic NL2SQL — AI-Powered Natural Language to SQL System

> **Internship Assignment — AI/ML Developer Intern**
> Built with Vanna AI 2.0 · FastAPI · Google Gemini · SQLite

---

## What This Does

This system lets you ask questions about a clinic database in **plain English** and get real SQL results — without writing any SQL yourself.

```
User: "Which doctor has the most appointments?"
  ↓
Vanna 2.0 Agent (Gemini 2.5 Flash)
  ↓
SELECT d.name, COUNT(a.id) AS appointment_count
FROM doctors d JOIN appointments a ON a.doctor_id = d.id
GROUP BY d.id ORDER BY appointment_count DESC LIMIT 1;
  ↓
{"message": "Dr. Arun Sharma has the most appointments with 52 total."}
```

---

## Architecture

```
User Question (plain English)
        ↓
  FastAPI /chat endpoint
        ↓
  Vanna 2.0 Agent
  ┌─────────────────────────────────┐
  │  GeminiLlmService               │  ← generates SQL
  │  DemoAgentMemory                │  ← learns from examples
  │  RunSqlTool                     │  ← executes SQL safely
  │  VisualizeDataTool              │  ← generates Plotly charts
  └─────────────────────────────────┘
        ↓
  SQL Validation (SELECT only)
        ↓
  SqliteRunner → clinic.db
        ↓
  Results + Chart returned as JSON
```

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.10+ |
| NL2SQL Engine | Vanna AI | 2.0.x |
| LLM | Google Gemini 2.5 Flash | Free tier |
| API Framework | FastAPI | Latest |
| Database | SQLite | Built-in |
| Charts | Plotly | Latest |
| UI | Swagger (auto-generated) | — |

**LLM Provider chosen: Google Gemini (Option A)**
Free key available at: https://aistudio.google.com/apikey

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Yashreddy05/clinic-nl2sql.git
cd clinic-nl2sql
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your Gemini API key:
# GOOGLE_API_KEY=your_key_here
```

Get a free key at: https://aistudio.google.com/apikey

### 5. Create the database

```bash
python setup_database.py
```

Expected output:
```
==================================================
  clinic.db created successfully!
==================================================
  Patients     : 200
  Doctors      : 15
  Appointments : 500
  Treatments   : 308
  Invoices     : 300
==================================================
```

### 6. Seed agent memory

```bash
python seed_memory.py
```

This teaches Vanna 15 example question→SQL pairs for a head start.

### 7. Start the API

```bash
uvicorn main:app --port 8000 --reload
```

API is live at: http://localhost:8000

---

## API Documentation

### POST /chat

Ask a question in plain English.

**Request:**
```json
{
  "question": "Show me the top 5 patients by total spending"
}
```

**Response:**
```json
{
  "message": "Here are the top 5 patients by total spending...",
  "sql_query": "SELECT p.first_name, p.last_name, SUM(i.total_amount)...",
  "columns": ["first_name", "last_name", "total_spending"],
  "rows": [["Aarav", "Sharma", 4850.00], ["Aditi", "Patel", 3920.50]],
  "row_count": 5,
  "chart": {"data": [...], "layout": {...}},
  "chart_type": "bar"
}
```

### GET /health

Check API and database status.

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "agent_memory_items": 15
}
```

### Interactive Docs

Open http://localhost:8000/docs for the Swagger UI — test all endpoints in the browser.

---

## One-Command Setup (as required)

```bash
pip install -r requirements.txt && python setup_database.py \
&& python seed_memory.py && uvicorn main:app --port 8000
```

---

## Project Structure

```
clinic-nl2sql/
├── setup_database.py   # Creates clinic.db with schema + dummy data
├── vanna_setup.py      # Vanna 2.0 Agent initialization
├── seed_memory.py      # Seeds 15 Q-A pairs into agent memory
├── main.py             # FastAPI application
├── requirements.txt    # All dependencies
├── .env.example        # API key template (rename to .env)
├── .gitignore          # Excludes .env and clinic.db
├── README.md           # This file
└── RESULTS.md          # Test results for 20 questions
```

---

## SQL Safety

All AI-generated SQL is validated before execution:
- Only `SELECT` statements are allowed
- Blocked keywords: `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `EXEC`, `GRANT`, `REVOKE`, `SHUTDOWN`
- System table access blocked: `sqlite_master`, `sqlite_sequence`

---

## Database Schema

The clinic database has 5 tables:
- **patients** — 200 patient records
- **doctors** — 15 doctors across 5 specializations
- **appointments** — 500 appointments over the past 12 months
- **treatments** — 308 treatment records linked to completed appointments
- **invoices** — 300 invoices with Paid/Pending/Overdue statuses

---

## Author

**Yashwanth Reddy**
- GitHub: [@Yashreddy05](https://github.com/Yashreddy05)
- LinkedIn: [yashwanth-reddyy05](https://www.linkedin.com/in/yashwanth-reddyy05)
