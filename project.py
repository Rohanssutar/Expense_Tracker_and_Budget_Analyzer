from __future__ import annotations
import csv
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Iterable, Optional


def parse_transactions(csv_source: Any) -> List[Dict[str, Any]]:
    """
    Parses a CSV file of transactions into a list of dictionaries.
    Each transaction includes: date, description, amount
    """
    close_after = False
    if isinstance(csv_source, str):
        f = open(csv_source, newline="", encoding="utf-8")
        close_after = True
    else:
        f = csv_source

    reader = csv.DictReader(f)
    out = []
    for row in reader:
        if not row:
            continue
        raw_date = row.get("date") or row.get("Date")
        desc = (row.get("description") or row.get("Description") or "").strip()
        amt_raw = row.get("amount") or row.get("Amount") or "0"

        # parse date robustly
        date_obj = None
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"):
            try:
                date_obj = datetime.strptime(raw_date.strip(), fmt).date()
                break
            except Exception:
                continue

        if date_obj is None:
            try:
                date_obj = datetime.fromisoformat(raw_date.strip()).date()
            except Exception:
                raise ValueError(f"Unrecognized date format: {raw_date}")

        # parse amount safely
        try:
            amount = float(amt_raw)
        except Exception:
            amount = float(amt_raw.replace(",", ""))

        out.append({"date": date_obj, "description": desc, "amount": amount})

    if close_after:
        f.close()
    return out


def categorize_transactions(
    transactions: Iterable[Dict[str, Any]],
    rules: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    """Categorizes transactions based on simple keyword rules."""
    if rules is None:
        rules = {
            "starbucks": "Coffee",
            "coffee": "Coffee",
            "uber": "Transport",
            "lyft": "Transport",
            "walmart": "Groceries",
            "supermarket": "Groceries",
            "salary": "Income",
            "payroll": "Income",
            "rent": "Housing",
            "mortgage": "Housing",
            "subscriptions": "Subscriptions",
            "netflix": "Subscriptions",
            "amazon": "Shopping",
            "grocery": "Groceries",
        }

    categorized = []
    for t in transactions:
        desc = (t.get("description") or "").lower()
        cat = "Uncategorized"
        for kw, c in rules.items():
            if kw in desc:
                cat = c
                break
        newt = dict(t)
        newt["category"] = cat
        categorized.append(newt)
    return categorized


def monthly_summary(transactions: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Generates a summary of transactions grouped by month."""
    summary: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"total": 0.0, "count": 0, "by_category": defaultdict(float)}
    )

    for t in transactions:
        date = t.get("date")
        if date is None:
            key = "unknown"
        else:
            key = f"{date.year:04d}-{date.month:02d}"

        amt = float(t.get("amount", 0.0))
        cat = t.get("category", "Uncategorized")

        summary[key]["total"] += amt
        summary[key]["count"] += 1
        summary[key]["by_category"][cat] += amt

    # Convert defaultdicts to normal dicts
    out = {}
    for k, v in summary.items():
        out[k] = {
            "total": v["total"],
            "count": v["count"],
            "by_category": dict(v["by_category"]),
        }
    return out


def recommend_budget(monthly: Dict[str, Dict[str, Any]], target_savings: float = 0.0) -> List[str]:
    """
    Provides budget recommendations based on the latest month's data.
    """
    if not monthly:
        return ["No data to produce recommendation."]

    # pick latest month by key sorting (YYYY-MM format sorts lexicographically)
    latest = (
        sorted(k for k in monthly.keys() if k != "unknown")[-1]
        if any(k != "unknown" for k in monthly.keys())
        else list(monthly.keys())[-1]
    )
    data = monthly[latest]
    total = data["total"]
    by_cat = data["by_category"]
    suggestions = []

    # If expenses are too high, suggest reductions
    if total < -500:
        top_spend = sorted(((abs(v), k) for k, v in by_cat.items()), reverse=True)[:3]
        for amt, cat in top_spend:
            suggestions.append(
                f"Consider reducing spending on {cat} by about ${amt*0.2:.2f} per month."
            )
    else:
        suggestions.append("Spending looks reasonable this month.")

    # Savings recommendation
    if target_savings > 0:
        current_savings = total if total > 0 else 0
        need = max(0.0, target_savings - current_savings)
        if need > 0:
            suggestions.append(
                f"To reach a target savings of ${target_savings:.2f}, increase monthly savings by ${need:.2f}."
            )
        else:
            suggestions.append("You are meeting or exceeding your savings target.")

    return suggestions


def main():
    """Main function to run the script from the command line."""
    if len(sys.argv) < 2:
        print("Usage: python project.py transactions.csv")
        print("Example CSV headers: date,description,amount")
        return

    path = sys.argv[1]
    try:
        tx = parse_transactions("sample.csv")
        cat = categorize_transactions(tx)
        summary = monthly_summary(cat)
        suggestions = recommend_budget(summary, target_savings=2000)
        for s in suggestions:
            print(s)
        
        print("\nMonthly summary (month: total, count):")
        for month, data in sorted(summary.items()):
            print(f"{month}: {data['total']:.2f}, {data['count']} transactions")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
