"""
seed_memory.py
──────────────
Pre-seeds the Vanna 2.0 DemoAgentMemory with 15 known-good
question → SQL pairs.

Run once before starting the API:
    python seed_memory.py
"""

from vanna_setup import agent, memory   # we'll export memory too

QA_PAIRS = [
    # ── Patient queries ──────────────────────────────────────────────────────
    {
        "question": "How many patients do we have?",
        "sql": "SELECT COUNT(*) AS total_patients FROM patients;",
    },
    {
        "question": "List all patients and their cities",
        "sql": "SELECT first_name, last_name, city FROM patients ORDER BY last_name;",
    },
    {
        "question": "How many male and female patients do we have?",
        "sql": "SELECT gender, COUNT(*) AS count FROM patients GROUP BY gender;",
    },
    {
        "question": "Which city has the most patients?",
        "sql": (
            "SELECT city, COUNT(*) AS patient_count FROM patients "
            "GROUP BY city ORDER BY patient_count DESC LIMIT 1;"
        ),
    },
    {
        "question": "List patients registered in the last 30 days",
        "sql": (
            "SELECT first_name, last_name, registered_date FROM patients "
            "WHERE registered_date >= date('now', '-30 days') "
            "ORDER BY registered_date DESC;"
        ),
    },
    # ── Doctor queries ───────────────────────────────────────────────────────
    {
        "question": "List all doctors and their specializations",
        "sql": "SELECT name, specialization, department FROM doctors ORDER BY specialization;",
    },
    {
        "question": "Which doctor has the most appointments?",
        "sql": (
            "SELECT d.name, COUNT(a.id) AS appointment_count "
            "FROM doctors d JOIN appointments a ON a.doctor_id = d.id "
            "GROUP BY d.id ORDER BY appointment_count DESC LIMIT 1;"
        ),
    },
    # ── Appointment queries ──────────────────────────────────────────────────
    {
        "question": "How many appointments are scheduled vs completed vs cancelled?",
        "sql": "SELECT status, COUNT(*) AS count FROM appointments GROUP BY status;",
    },
    {
        "question": "Show appointments for last month",
        "sql": (
            "SELECT a.id, p.first_name, p.last_name, d.name AS doctor, "
            "a.appointment_date, a.status "
            "FROM appointments a "
            "JOIN patients p ON p.id = a.patient_id "
            "JOIN doctors  d ON d.id = a.doctor_id "
            "WHERE a.appointment_date >= date('now', '-1 month') "
            "ORDER BY a.appointment_date DESC;"
        ),
    },
    {
        "question": "How many cancelled appointments were there last quarter?",
        "sql": (
            "SELECT COUNT(*) AS cancelled_count FROM appointments "
            "WHERE status = 'Cancelled' "
            "AND appointment_date >= date('now', '-3 months');"
        ),
    },
    # ── Financial queries ────────────────────────────────────────────────────
    {
        "question": "What is the total revenue?",
        "sql": "SELECT SUM(total_amount) AS total_revenue FROM invoices;",
    },
    {
        "question": "Show revenue by doctor",
        "sql": (
            "SELECT d.name, SUM(i.total_amount) AS total_revenue "
            "FROM invoices i "
            "JOIN appointments a ON a.patient_id = i.patient_id "
            "JOIN doctors d ON d.id = a.doctor_id "
            "GROUP BY d.name ORDER BY total_revenue DESC;"
        ),
    },
    {
        "question": "Show unpaid invoices",
        "sql": (
            "SELECT p.first_name, p.last_name, i.total_amount, "
            "i.paid_amount, i.status, i.invoice_date "
            "FROM invoices i "
            "JOIN patients p ON p.id = i.patient_id "
            "WHERE i.status IN ('Pending', 'Overdue') "
            "ORDER BY i.status, i.invoice_date;"
        ),
    },
    # ── Time-based queries ───────────────────────────────────────────────────
    {
        "question": "Show monthly appointment count for the past 6 months",
        "sql": (
            "SELECT strftime('%Y-%m', appointment_date) AS month, "
            "COUNT(*) AS total_appointments "
            "FROM appointments "
            "WHERE appointment_date >= date('now', '-6 months') "
            "GROUP BY month ORDER BY month;"
        ),
    },
    {
        "question": "Top 5 patients by total spending",
        "sql": (
            "SELECT p.first_name, p.last_name, "
            "SUM(i.total_amount) AS total_spending "
            "FROM invoices i "
            "JOIN patients p ON p.id = i.patient_id "
            "GROUP BY i.patient_id "
            "ORDER BY total_spending DESC LIMIT 5;"
        ),
    },
]


def seed():
    from vanna.integrations.local.agent_memory import DemoAgentMemory

    # Get memory from agent
    mem = agent.agent_memory

    print("Seeding agent memory with", len(QA_PAIRS), "Q-A pairs...")
    print("Memory methods available:", [m for m in dir(mem) if not m.startswith("_")])
    print()

    success = 0
    for i, pair in enumerate(QA_PAIRS, 1):
        try:
            # Try saving tool usage
            mem.save_tool_usage(
                question=pair["question"],
                tool_name="run_sql",
                args={"sql": pair["sql"]}
            )
            print(f"[{i:02d}] TOOL saved")
            success += 1

        except Exception as e1:
            print(f"[{i:02d}] TOOL FAILED → trying text memory")

        try:
            # Fallback to text memory
            mem.save_text_memory(
                f"Q: {pair['question']}\nSQL: {pair['sql']}",
                context="training"
            )
            print(f"[{i:02d}] TEXT saved")
            success += 1

        except Exception as e2:
            print(f"[{i:02d}] FAILED: {e1} | {e2}")

    print(f"\nDone! {success}/{len(QA_PAIRS)} pairs saved.")
    print()
    print(f"Done! {success}/{len(QA_PAIRS)} pairs saved.")
    print("Start the API with:  uvicorn main:app --port 8000 --reload")


if __name__ == "__main__":
    seed()