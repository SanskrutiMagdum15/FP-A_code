# FP&A Agent (Mini CFO Copilot)

A lightweight FP&A (Financial Planning & Analysis) copilot built with **Python + Streamlit**.  
It allows to ask natural language financial questions and it computes metrics like **Revenue, Gross Margin, Opex, EBITDA, and Cash Runway**.


## Features

- Revenue (Actual vs Budget)
- Gross Margin % = (Revenue – COGS) / Revenue
- Opex breakdown by category
- EBITDA = Revenue – COGS – Opex
- Cash runway = Cash ÷ Avg monthly burn (last 3 months)
- Interactive charts with Streamlit

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SanskrutiMagdum15/FP-A_code.git
cd FP-A_code

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Install dependencies:
pip install -r requirements.txt

```

## Usage
Run the Streamlit app:
streamlit run app.py
Then open http://localhost:8501 in your browser.

## Running Tests
Tests are written using pytest:
pytest tests/

## Example Questions
1. Revenue vs budget for June 2025
2. Gross margin last 3 months
3. Show me Opex breakdown for 2025
4. What is the EBITDA in June?
5. Cash runway months left

## Tech Stack
Python 3.9+, Streamlit (frontend + backend UI), Pandas (data processing), Matplotlib (charting), Pytest (testing)

## Author
Created by Sanskruti Magdum
