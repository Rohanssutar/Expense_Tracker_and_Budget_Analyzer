import io
from project import parse_transactions, categorize_transactions, monthly_summary


def test_parse_transactions_basic():
    csv = io.StringIO("""
    date,description,amount
    2025-01-05,Coffee Shop,-3.50
    2025-01-06,Salary,2000
    """)
    tx = parse_transactions(csv)
    assert len(tx) == 2
    assert any(t['description'] == 'Coffee Shop' and abs(t['amount'] + 3.5) < 1e-9 for t in tx)
    assert any(t['description'] == 'Salary' and abs(t['amount'] - 2000) < 1e-9 for t in tx)


def test_categorize_transactions_rules_and_default():
    txs = [
    {"date": None, "description": "Starbucks downtown", "amount": -4.25},
    {"date": None, "description": "Unknown Merchant", "amount": -12.0},
    ]
    categorized = categorize_transactions(txs)
    assert categorized[0]["category"] == "Coffee"
    assert categorized[1]["category"] == "Uncategorized"


def test_monthly_summary_aggregation():
    txs = [
    {"date": __import__('datetime').date(2025, 1, 1), "description": "A", "amount": -10.0, "category": "X"},
    {"date": __import__('datetime').date(2025, 1, 5), "description": "B", "amount": -5.0, "category": "Y"},
    {"date": __import__('datetime').date(2025, 2, 1), "description": "C", "amount": 100.0, "category": "Income"},
    ]
    s = monthly_summary(txs)
    assert s['2025-01']['total'] == -15.0
    assert s['2025-01']['count'] == 2
    assert s['2025-01']['by_category']['X'] == -10.0
    assert s['2025-02']['total'] == 100.0
