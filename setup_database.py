import sqlite3
import random
from datetime import datetime, timedelta, date

DB_PATH = "clinic.db"

# ── Seed data ──────────────────────────────────────────────────────────────────

FIRST_NAMES = [
    "Aarav","Aditi","Akash","Anil","Anjali","Arjun","Deepa","Divya","Farhan",
    "Ganesh","Geeta","Harish","Ishaan","Jaya","Kiran","Lakshmi","Madhav","Meena",
    "Mohan","Neeraj","Neha","Nikhil","Pallavi","Pooja","Pradeep","Priya","Rahul",
    "Rajesh","Rakesh","Ramesh","Ravi","Rekha","Rita","Rohit","Sachin","Sangeeta",
    "Sanjay","Santosh","Shalini","Shyam","Sneha","Suresh","Swati","Tanvi","Usha",
    "Varun","Vijay","Vikram","Vinod","Yamini","Zara","Kabir","Leela","Mihir",
    "Nisha","Omkar","Poonam","Ramya","Sunil","Tara","Umesh","Veena","Yash",
    "Aditya","Bhavna","Chetan","Disha","Ekta","Faisal","Gayatri","Hemant",
    "Isha","Jagdish","Kavya","Laxman","Manju","Naveen","Ojas","Preeti","Qasim",
    "Rajani","Shivangi","Tarun","Urmila","Vivek","Wasim","Xena","Yogesh","Zoya"
]

LAST_NAMES = [
    "Sharma","Verma","Patel","Singh","Kumar","Gupta","Joshi","Mehta","Nair",
    "Reddy","Rao","Pillai","Iyer","Mishra","Chauhan","Yadav","Tiwari","Pandey",
    "Agarwal","Bose","Chopra","Das","Fernandez","Goel","Hegde","Jain","Kapoor",
    "Lal","Malhotra","Nambiar","Oberoi","Prasad","Qureshi","Roy","Saxena",
    "Trivedi","Upadhyay","Venkatesan","Walia","Yadav","Zaveri"
]

CITIES = [
    "Hyderabad","Bengaluru","Mumbai","Chennai","Pune","Delhi","Kolkata","Ahmedabad","Jaipur","Lucknow"
]

SPECIALIZATIONS = ["Dermatology","Cardiology","Orthopedics","General","Pediatrics"]

DEPARTMENTS = {
    "Dermatology": "Skin & Hair",
    "Cardiology":  "Heart & Vascular",
    "Orthopedics": "Bone & Joint",
    "General":     "General Medicine",
    "Pediatrics":  "Child Health",
}

DOCTOR_NAMES = [
    ("Dr. Arun Sharma",      "Dermatology"),
    ("Dr. Bhavna Mehta",     "Dermatology"),
    ("Dr. Chandra Reddy",    "Dermatology"),
    ("Dr. Deepak Verma",     "Cardiology"),
    ("Dr. Esha Gupta",       "Cardiology"),
    ("Dr. Farooq Khan",      "Cardiology"),
    ("Dr. Geeta Iyer",       "Orthopedics"),
    ("Dr. Harish Pillai",    "Orthopedics"),
    ("Dr. Isha Nair",        "Orthopedics"),
    ("Dr. Jatin Patel",      "General"),
    ("Dr. Kavya Singh",      "General"),
    ("Dr. Lokesh Joshi",     "General"),
    ("Dr. Manisha Rao",      "Pediatrics"),
    ("Dr. Nikhil Mishra",    "Pediatrics"),
    ("Dr. Omkar Tiwari",     "Pediatrics"),
]

TREATMENTS = {
    "Dermatology": [
        ("Skin Biopsy", 1500, 45),
        ("Acne Treatment", 800, 30),
        ("Chemical Peel", 2500, 60),
        ("Laser Therapy", 4500, 90),
        ("Eczema Consultation", 600, 20),
    ],
    "Cardiology": [
        ("ECG", 500, 20),
        ("Echocardiogram", 3000, 45),
        ("Stress Test", 2000, 60),
        ("Holter Monitoring", 2500, 30),
        ("Angiography", 5000, 120),
    ],
    "Orthopedics": [
        ("X-Ray & Consultation", 700, 30),
        ("Physiotherapy Session", 800, 45),
        ("Joint Injection", 2000, 30),
        ("Fracture Management", 3500, 60),
        ("Bone Density Scan", 1500, 30),
    ],
    "General": [
        ("General Consultation", 300, 15),
        ("Blood Panel", 600, 10),
        ("Vaccination", 400, 10),
        ("Diabetes Management", 500, 20),
        ("Thyroid Test", 700, 10),
    ],
    "Pediatrics": [
        ("Child Wellness Check", 400, 20),
        ("Immunization", 350, 15),
        ("Growth Assessment", 500, 20),
        ("Fever Consultation", 300, 15),
        ("Nutrition Counselling", 600, 25),
    ],
}

STATUSES      = ["Scheduled", "Completed", "Cancelled", "No-Show"]
STATUS_WEIGHTS= [10, 60, 20, 10]
INV_STATUSES  = ["Paid", "Pending", "Overdue"]
INV_WEIGHTS   = [60, 25, 15]

# ── Helpers ────────────────────────────────────────────────────────────────────

def rand_date(start_days_ago: int, end_days_ago: int = 0) -> str:
    delta = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=delta)).strftime("%Y-%m-%d")

def rand_datetime(start_days_ago: int, end_days_ago: int = 0) -> str:
    delta   = random.randint(end_days_ago, start_days_ago)
    hour    = random.randint(8, 17)
    minute  = random.choice([0, 15, 30, 45])
    return (datetime.now() - timedelta(days=delta, hours=-(hour), minutes=-(minute))).strftime("%Y-%m-%d %H:%M:%S")

def rand_phone():
    if random.random() < 0.15:
        return None
    return f"+91-{random.randint(7000000000, 9999999999)}"

def rand_email(first, last):
    if random.random() < 0.1:
        return None
    domains = ["gmail.com","yahoo.com","hotmail.com","outlook.com","rediffmail.com"]
    return f"{first.lower()}.{last.lower()}{random.randint(1,99)}@{random.choice(domains)}"

# ── Main build ─────────────────────────────────────────────────────────────────

def build():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # ── Schema ─────────────────────────────────────────────────────────────────
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    DROP TABLE IF EXISTS invoices;
    DROP TABLE IF EXISTS treatments;
    DROP TABLE IF EXISTS appointments;
    DROP TABLE IF EXISTS doctors;
    DROP TABLE IF EXISTS patients;

    CREATE TABLE patients (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name      TEXT    NOT NULL,
        last_name       TEXT    NOT NULL,
        email           TEXT,
        phone           TEXT,
        date_of_birth   DATE,
        gender          TEXT,
        city            TEXT,
        registered_date DATE
    );

    CREATE TABLE doctors (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT    NOT NULL,
        specialization  TEXT,
        department      TEXT,
        phone           TEXT
    );

    CREATE TABLE appointments (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id       INTEGER REFERENCES patients(id),
        doctor_id        INTEGER REFERENCES doctors(id),
        appointment_date DATETIME,
        status           TEXT,
        notes            TEXT
    );

    CREATE TABLE treatments (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id    INTEGER REFERENCES appointments(id),
        treatment_name    TEXT,
        cost              REAL,
        duration_minutes  INTEGER
    );

    CREATE TABLE invoices (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id    INTEGER REFERENCES patients(id),
        invoice_date  DATE,
        total_amount  REAL,
        paid_amount   REAL,
        status        TEXT
    );
    """)

    # ── Doctors (15) ───────────────────────────────────────────────────────────
    doctor_rows = []
    for name, spec in DOCTOR_NAMES:
        doctor_rows.append((
            name, spec,
            DEPARTMENTS[spec],
            rand_phone() or f"+91-{random.randint(7000000000,9999999999)}"
        ))
    cur.executemany(
        "INSERT INTO doctors (name,specialization,department,phone) VALUES (?,?,?,?)",
        doctor_rows
    )
    doctor_ids = [r[0] for r in cur.execute("SELECT id FROM doctors").fetchall()]

    # build a map: doctor_id -> specialization
    doc_spec = {
        row[0]: row[1]
        for row in cur.execute("SELECT id, specialization FROM doctors").fetchall()
    }

    # give busier doctors higher weight
    busy_doctors = doctor_ids[:5]
    doctor_weights = [4 if d in busy_doctors else 1 for d in doctor_ids]

    # ── Patients (200) ─────────────────────────────────────────────────────────
    patient_rows = []
    names_pool   = [(f, l) for f in FIRST_NAMES for l in LAST_NAMES]
    random.shuffle(names_pool)
    for i in range(200):
        first, last = names_pool[i % len(names_pool)]
        dob  = rand_date(365*60, 365*18)   # 18–60 yrs old
        reg  = rand_date(365, 0)
        patient_rows.append((
            first, last,
            rand_email(first, last),
            rand_phone(),
            dob,
            random.choice(["M","F"]),
            random.choice(CITIES),
            reg,
        ))
    cur.executemany(
        "INSERT INTO patients (first_name,last_name,email,phone,date_of_birth,gender,city,registered_date) VALUES (?,?,?,?,?,?,?,?)",
        patient_rows
    )
    patient_ids = [r[0] for r in cur.execute("SELECT id FROM patients").fetchall()]

    # give repeat-visitor patients higher weight
    repeat_patients = random.sample(patient_ids, 40)
    patient_weights  = [5 if p in repeat_patients else 1 for p in patient_ids]

    # ── Appointments (500) ─────────────────────────────────────────────────────
    appt_rows = []
    for _ in range(500):
        pid    = random.choices(patient_ids, weights=patient_weights)[0]
        did    = random.choices(doctor_ids,  weights=doctor_weights)[0]
        dt     = rand_datetime(365)
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
        notes  = None if random.random() < 0.4 else f"Follow-up on {rand_date(30)}"
        appt_rows.append((pid, did, dt, status, notes))
    cur.executemany(
        "INSERT INTO appointments (patient_id,doctor_id,appointment_date,status,notes) VALUES (?,?,?,?,?)",
        appt_rows
    )

    # ── Treatments (350, only for Completed appts) ─────────────────────────────
    completed_appts = cur.execute(
        "SELECT a.id, a.doctor_id FROM appointments a WHERE a.status='Completed'"
    ).fetchall()
    random.shuffle(completed_appts)
    treat_rows = []
    for appt_id, did in completed_appts[:350]:
        spec = doc_spec[did]
        name, cost, dur = random.choice(TREATMENTS[spec])
        cost += random.uniform(-50, 200)   # add some variance
        cost  = round(max(50, cost), 2)
        treat_rows.append((appt_id, name, cost, dur))
    cur.executemany(
        "INSERT INTO treatments (appointment_id,treatment_name,cost,duration_minutes) VALUES (?,?,?,?)",
        treat_rows
    )

    # ── Invoices (300) ─────────────────────────────────────────────────────────
    invoice_patient_ids = random.choices(patient_ids, k=300)
    inv_rows = []
    for pid in invoice_patient_ids:
        total   = round(random.uniform(300, 5000), 2)
        status  = random.choices(INV_STATUSES, weights=INV_WEIGHTS)[0]
        paid    = total if status == "Paid" else round(random.uniform(0, total * 0.5), 2)
        inv_date = rand_date(365)
        inv_rows.append((pid, inv_date, total, paid, status))
    cur.executemany(
        "INSERT INTO invoices (patient_id,invoice_date,total_amount,paid_amount,status) VALUES (?,?,?,?,?)",
        inv_rows
    )

    conn.commit()

    # ── Summary ────────────────────────────────────────────────────────────────
    print("=" * 50)
    print("  clinic.db created successfully!")
    print("=" * 50)
    print(f"  Patients     : {cur.execute('SELECT COUNT(*) FROM patients').fetchone()[0]}")
    print(f"  Doctors      : {cur.execute('SELECT COUNT(*) FROM doctors').fetchone()[0]}")
    print(f"  Appointments : {cur.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]}")
    print(f"  Treatments   : {cur.execute('SELECT COUNT(*) FROM treatments').fetchone()[0]}")
    print(f"  Invoices     : {cur.execute('SELECT COUNT(*) FROM invoices').fetchone()[0]}")
    print("=" * 50)
    conn.close()

if __name__ == "__main__":
    random.seed(42)
    build()