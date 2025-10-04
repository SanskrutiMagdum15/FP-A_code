import pandas as pd
from agent import metrics

def make_df(rows):
    df = pd.DataFrame(rows)
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month
    return df

def test_revenue_vs_budget():
    actuals = make_df([
        {"month": "2025-06", "entity": "TestCo", "account_category": "Revenue", "amount": 1000}
    ])
    budget = make_df([
        {"month": "2025-06", "entity": "TestCo", "account_category": "Revenue", "amount": 900}
    ])

    res = metrics.revenue_vs_budget(actuals, budget, 6, 2025)
    assert res["actual"] == 1000
    assert res["budget"] == 900
    assert res["variance"] == 100

def test_gross_margin():
    actuals = make_df([
        {"month": "2025-10", "entity": "TestCo", "account_category": "Revenue", "amount": 1000},
        {"month": "2025-10", "entity": "TestCo", "account_category": "COGS", "amount": 200},
        {"month": "2025-11", "entity": "TestCo", "account_category": "Revenue", "amount": 1200},
        {"month": "2025-11", "entity": "TestCo", "account_category": "COGS", "amount": 300}
    ])
    res = metrics.gross_margin(actuals, months=2)
    assert isinstance(res, list)
    assert "gross_margin_pct" in res[0]
    assert round(res[0]["gross_margin_pct"], 2) == 0.8

def test_opex_breakdown():
    actuals = make_df([
        {"month": "2025-06", "entity": "TestCo", "account_category": "Opex:Admin", "amount": 200},
        {"month": "2025-06", "entity": "TestCo", "account_category": "Opex:Sales", "amount": 300}
    ])
    res = metrics.opex_breakdown(actuals, 6, 2025)
    cats = [r["account_category"] for r in res]
    assert "Opex:Admin" in cats
    assert "Opex:Sales" in cats
    amounts = {r["account_category"]: r["amount"] for r in res}
    assert amounts["Opex:Admin"] == 200
    assert amounts["Opex:Sales"] == 300

def test_ebitda():
    actuals = make_df([
        {"month": "2025-06", "entity": "TestCo", "account_category": "Revenue", "amount": 1000},
        {"month": "2025-06", "entity": "TestCo", "account_category": "COGS", "amount": 200},
        {"month": "2025-06", "entity": "TestCo", "account_category": "Opex:Admin", "amount": 300}
    ])
    res = metrics.ebitda(actuals, 6, 2025)
    assert res["ebitda"] == 500

def test_cash_runway():
    actuals = make_df([
        {"month": "2025-04", "entity": "TestCo", "account_category": "Net Income", "amount": -100},
        {"month": "2025-05", "entity": "TestCo", "account_category": "Net Income", "amount": -200},
        {"month": "2025-06", "entity": "TestCo", "account_category": "Net Income", "amount": -300}
    ])
    cash = make_df([
        {"month": "2025-06", "entity": "TestCo", "cash_usd": 1200}
    ])
    res = metrics.cash_runway(cash, actuals)
    assert "cash_runway_months" in res
    assert res["cash_runway_months"] > 0
