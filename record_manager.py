import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "training_records.csv")
FIELDS = ["Employee ID", "Employee Name", "Department", "Program", "Status", "Score", "Date"]

def ensure_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def load_records():
    ensure_file()
    with open(FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_all(records):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

def validate_record(data):
    for field in ["Employee ID", "Employee Name", "Department", "Program", "Score", "Date"]:
        if not data[field]:
            raise ValueError(f"{field} cannot be empty.")
    try:
        score = float(data["Score"])
    except ValueError:
        raise ValueError("Score must be a number.")
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")

    try:
        datetime.strptime(data["Date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be valid and in YYYY-MM-DD format.")

def add_record(data, records):
    validate_record(data)
    if any(r["Employee ID"] == data["Employee ID"] and r["Program"] == data["Program"] for r in records):
        raise ValueError("This employee already has a record for this program.")
    records.append(data)
    save_all(records)

def delete_record(index, records):
    if 0 <= index < len(records):
        records.pop(index)
        save_all(records)

def search_records(records, keyword):
    if not keyword:
        return records
    k = keyword.lower()
    return [r for r in records if any(k in str(v).lower() for v in r.values())]
