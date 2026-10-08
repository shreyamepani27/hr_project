from collections import Counter
import pandas as pd
import numpy as np

def completion_statistics(records):
    total = len(records)
    completed = sum(r["Status"] == "Completed" for r in records)
    in_progress = sum(r["Status"] == "In Progress" for r in records)
    rate = (completed / total * 100) if total else 0
    return {"total": total, "completed": completed, "in_progress": in_progress, "rate": rate}

def department_statistics(records):
    return Counter(r["Department"] for r in records)

def program_statistics(records):
    return Counter(r["Program"] for r in records)

def status_statistics(records):
    return Counter(r["Status"] for r in records)

def average_scores_by_program(records):
    if not records:
        return {}
    df = pd.DataFrame(records)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    result = df.groupby("Program")["Score"].mean().round(2)
    return result.to_dict()

def monthly_completion(records):
    if not records:
        return {}
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df[df["Status"] == "Completed"].dropna(subset=["Date"])
    if df.empty:
        return {}
    result = df.groupby(df["Date"].dt.to_period("M")).size()
    return {str(k): int(v) for k, v in result.items()}

def score_array(records):
    return np.array([float(r["Score"]) for r in records if r.get("Score")])
