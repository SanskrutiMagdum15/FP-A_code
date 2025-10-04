import pandas as pd

DATA_DIR = "fixtures"

def load_data():
    actuals = pd.read_csv(f"{DATA_DIR}/actuals.csv")
    budget = pd.read_csv(f"{DATA_DIR}/budget.csv")
    fx = pd.read_csv(f"{DATA_DIR}/fx.csv")
    cash = pd.read_csv(f"{DATA_DIR}/cash.csv")

    actuals = actuals.loc[:, ~actuals.columns.str.contains("Unnamed")]
    budget = budget.loc[:, ~budget.columns.str.contains("Unnamed")]
    fx = fx.loc[:, ~fx.columns.str.contains("Unnamed")]
    cash = cash.loc[:, ~cash.columns.str.contains("Unnamed")]

    for df in [actuals, budget, fx, cash]:
        df["month"] = pd.to_datetime(df["month"], format="%Y-%m", errors="coerce")
        df["year"] = df["month"].dt.year
        df["month_num"] = df["month"].dt.month


    if "cash_usd" in cash.columns:
        cash["cash_usd"] = pd.to_numeric(cash["cash_usd"], errors="coerce")
        cash = cash.dropna(subset=["cash_usd"])

    return actuals, budget, fx, cash
