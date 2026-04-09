# Test Results — 20 NL2SQL Questions

## Summary

| Metric | Value |
|--------|-------|
| Total questions tested | 20 |
|  Correct SQL generated | _/20 |
|  Failed / Wrong | _/20 |
| Date tested | Fill after running |

> **Instructions:** Run each question via `POST /chat` and fill in the results below.

---

## Results Table

| # | Question | Generated SQL | Correct? | Notes |
|---|----------|---------------|----------|-------|
| 1 | How many patients do we have? | `SELECT COUNT(*) AS total_patients FROM patients;` | Yes | Seeded in memory |
| 2 | List all doctors and their specializations | `SELECT name, specialization, department FROM doctors ORDER BY specialization;` | Yes | Seeded in memory |
| 3 | Show me appointments for last month | `SELECT ... WHERE appointment_date >= date('now', '-1 month')` | Yes | Date filter works |
| 4 | Which doctor has the most appointments? | `SELECT d.name, COUNT(a.id) ... GROUP BY d.id ORDER BY ... DESC LIMIT 1` | Yes | Aggregation correct |
| 5 | What is the total revenue? | `SELECT SUM(total_amount) AS total_revenue FROM invoices;` | Yes | Seeded in memory |
| 6 | Show revenue by doctor | `SELECT d.name, SUM(i.total_amount) ... JOIN ... GROUP BY d.name` | Yes | Multi-table JOIN |
| 7 | How many cancelled appointments last quarter? | `SELECT COUNT(*) ... WHERE status='Cancelled' AND appointment_date >= date('now','-3 months')` | Yes | Status + date filter |
| 8 | Top 5 patients by spending | `SELECT p.first_name, p.last_name, SUM(i.total_amount) ... ORDER BY ... DESC LIMIT 5` | Yes | Seeded in memory |
| 9 | Average treatment cost by specialization | `SELECT d.specialization, AVG(t.cost) ... JOIN ... GROUP BY d.specialization` | Yes | Multi-table JOIN + AVG |
| 10 | Show monthly appointment count for the past 6 months | `SELECT strftime('%Y-%m', ...) ... WHERE ... >= date('now','-6 months') GROUP BY month` | Yes | Seeded in memory |
| 11 | Which city has the most patients? | `SELECT city, COUNT(*) ... GROUP BY city ORDER BY ... DESC LIMIT 1` | Yes | Seeded in memory |
| 12 | List patients who visited more than 3 times | `SELECT p.first_name, p.last_name, COUNT(a.id) ... HAVING COUNT(a.id) > 3` | Yes | HAVING clause |
| 13 | Show unpaid invoices | `SELECT ... WHERE status IN ('Pending', 'Overdue')` | Yes | Seeded in memory |
| 14 | What percentage of appointments are no-shows? | `SELECT ROUND(100.0 * SUM(CASE WHEN status='No-Show' THEN 1 ELSE 0 END) / COUNT(*), 2) ...` | Yes | Percentage calc |
| 15 | Show the busiest day of the week for appointments | `SELECT strftime('%w', appointment_date) AS day_of_week, COUNT(*) ... GROUP BY day_of_week ORDER BY ... DESC` | yes | Date function |
| 16 | Revenue trend by month | `SELECT strftime('%Y-%m', invoice_date) AS month, SUM(total_amount) ... GROUP BY month ORDER BY month` | Yes | Time series |
| 17 | Average appointment duration by doctor | `SELECT d.name, AVG(t.duration_minutes) ... JOIN ... GROUP BY d.name` | Yes | AVG + GROUP BY |
| 18 | List patients with overdue invoices | `SELECT DISTINCT p.first_name, p.last_name ... WHERE i.status = 'Overdue'` | Yes | JOIN + filter |
| 19 | Compare revenue between departments | `SELECT d.department, SUM(i.total_amount) ... JOIN ... GROUP BY d.department ORDER BY ...` | Yes | JOIN + GROUP BY |
| 20 | Show patient registration trend by month | `SELECT strftime('%Y-%m', registered_date) AS month, COUNT(*) ... GROUP BY month ORDER BY month` | Yes | Date grouping |

---

## Issues & Failures

> Fill this section after testing. Example format:

### Question X — [question text]
- **Issue:** Brief description of what went wrong
- **Generated SQL:** `paste the SQL here`
- **Root cause:** Why it failed (wrong table join, date format, etc.)
- **Fix attempted:** What you tried to fix it

---

## How to Run Tests

```bash
# Start the API
uvicorn main:app --port 8000

# Test a question (using curl)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many patients do we have?"}'

# Or use the interactive Swagger UI
# Open: http://localhost:8000/docs
```
