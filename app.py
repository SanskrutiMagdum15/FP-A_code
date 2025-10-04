import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from agent.utils import load_data
from agent.intent import classify_and_run

st.title("FP&A Agent (Mini CFO Copilot)")

actuals, budget, fx, cash = load_data()

question = st.text_input("Ask a financial question:")

ask_button = st.button("Ask", disabled=(len(question.strip()) == 0))

if ask_button and question.strip():
    result = classify_and_run(question, actuals, budget, fx, cash)
    
    st.write("Answer")

    if isinstance(result, dict) and "error" in result:
        st.warning(result["error"])
        st.info("Example questions: 'Revenue vs budget', 'Gross margin last 3 months', 'Opex breakdown', 'EBITDA', 'Cash runway'.")
    else:
        st.write(result)

        df = None
        if isinstance(result, list):
            df = pd.DataFrame(result)
        elif isinstance(result, dict):
            df = pd.DataFrame([result])

        if df is not None and "gross_margin_pct" in df.columns:
            fig, ax = plt.subplots()
            df.plot(x="month_num", y="gross_margin_pct", kind="line", ax=ax, marker="o")
            ax.set_ylabel("Gross Margin %")
            st.pyplot(fig)

        if df is not None and "account_category" in df.columns:
            fig, ax = plt.subplots()
            df.plot(x="account_category", y="amount", kind="bar", ax=ax, legend=False)
            ax.set_ylabel("Opex")
            st.pyplot(fig)

        if df is not None and {"actual", "budget"}.issubset(df.columns):
            fig, ax = plt.subplots()
            df[["actual", "budget"]].plot(kind="bar", ax=ax)
            ax.set_ylabel("Revenue (USD)")
            ax.set_title("Revenue vs Budget")
            st.pyplot(fig)
