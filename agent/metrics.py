import pandas as pd

def revenue_vs_budget(actuals, budget, month, year):
    a = actuals[
        (actuals["month_num"] == month) &
        (actuals["year"] == year) &
        (actuals["account_category"] == "Revenue")
    ]["amount"].sum()

    b = budget[
        (budget["month_num"] == month) &
        (budget["year"] == year) &
        (budget["account_category"] == "Revenue")
    ]["amount"].sum()

    return {"actual": int(a), "budget": int(b), "variance": int(a - b)}


def gross_margin(actuals, months=3):
    rev = actuals[actuals["account_category"] == "Revenue"].groupby(["year", "month_num"])["amount"].sum()
    cogs = actuals[actuals["account_category"] == "COGS"].groupby(["year", "month_num"])["amount"].sum()

    df = pd.DataFrame({"revenue": rev, "cogs": cogs}).reset_index()
    df["gross_margin_pct"] = (df["revenue"] - df["cogs"]) / df["revenue"]

    df["revenue"] = df["revenue"].astype(int)
    df["cogs"] = df["cogs"].astype(int)
    df["gross_margin_pct"] = df["gross_margin_pct"].astype(float)

    return df.tail(months).to_dict(orient="records")


def opex_breakdown(actuals, month, year):
    df = actuals[
        (actuals["month_num"] == month) &
        (actuals["year"] == year) &
        (actuals["account_category"].str.startswith("Opex"))
    ]
    breakdown = df.groupby("account_category")["amount"].sum().reset_index()
    breakdown["amount"] = breakdown["amount"].astype(int)
    return breakdown.to_dict(orient="records")


def ebitda(actuals, month, year):
    df = actuals[(actuals["month_num"] == month) & (actuals["year"] == year)]
    rev = df[df["account_category"] == "Revenue"]["amount"].sum()
    cogs = df[df["account_category"] == "COGS"]["amount"].sum()
    opex = df[df["account_category"].str.startswith("Opex")]["amount"].sum()
    return {"ebitda": int(rev - cogs - opex)}


def cash_runway(cash, actuals):
    if "cash_usd" not in cash.columns or cash.empty:
        return {"cash_runway_months": None, "note": "No cash data available"}

    cash["cash_usd"] = pd.to_numeric(cash["cash_usd"], errors="coerce")
    cash = cash.dropna(subset=["cash_usd"])
    if cash.empty:
        return {"cash_runway_months": None, "note": "Cash column is empty or invalid"}

    latest_cash = float(cash.tail(1)["cash_usd"].values[0])

    if "account_category" in actuals.columns and "Net Income" in actuals["account_category"].values:
        ni = actuals[actuals["account_category"] == "Net Income"].tail(3)["amount"].mean()
        avg_burn = -ni
    else:
        avg_burn = (actuals.tail(3)["amount"].sum() / -3)

    if avg_burn <= 0 or pd.isna(avg_burn):
        return {"cash_runway_months": float("inf"), "note": "Company is not burning cash"}

    return {"cash_runway_months": round(latest_cash / avg_burn, 1)}
