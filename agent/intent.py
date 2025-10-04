import re
from . import metrics

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12
}

def extract_date(text):
    text = text.lower()
    month = None
    year = None

    for m, num in MONTHS.items():
        if m in text:
            month = num
            break

    match = re.search(r"(20\d{2})", text)
    if match:
        year = int(match.group(1))

    return month, year

def classify_and_run(question, actuals, budget, fx, cash):
    q = question.lower()
    month, year = extract_date(q)

    if month is None:
        month = 6
    if year is None:
        year = 2025

    if ("revenue" in q and "budget" in q) or ("revenue vs" in q) or ("sales vs budget" in q):
        return metrics.revenue_vs_budget(actuals, budget, month=month, year=year)

    elif "gross margin" in q or "gm" in q or "margin" in q:
        return metrics.gross_margin(actuals)

    elif "opex" in q or "operating expense" in q or "expenses" in q:
        return metrics.opex_breakdown(actuals, month=month, year=year)

    elif "ebitda" in q or "profit" in q or "earnings" in q or "income" in q:
        return metrics.ebitda(actuals, month=month, year=year)

    elif "cash runway" in q or "runway" in q or ("cash" in q and "months" in q):
        return metrics.cash_runway(cash, actuals)

    else:
        return {
            "error": "Sorry, I don't understand the question.",
            "hint": "Try asking: 'Revenue vs budget June 2025', 'Gross margin last 3 months', 'Opex breakdown', 'EBITDA', or 'Cash runway'."
        }
