"""PayoffPath: AI-assisted loan payoff planner built with Streamlit."""
import pandas as pd
import streamlit as st

from calculator import amortization_schedule

st.set_page_config(page_title="PayoffPath | Loan Payoff Planner", page_icon="💸", layout="wide")
st.markdown("""
<style>
.block-container {max-width: 1120px; padding-top: 2rem;}
h1, h2, h3 {letter-spacing: -0.025em;}
[data-testid="stMetricValue"] {font-weight: 750;}
.eyebrow {font-size: .78rem; font-weight: 750; letter-spacing: .13em; color: #2B7A78;}
.subhead {color: #637384; font-size: 1.05rem;}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">PERSONAL FINANCE TOOL</p>', unsafe_allow_html=True)
st.title("💸 PayoffPath")
st.markdown(
    '<p class="subhead">Know what your loan really costs—and see how much faster '
    'you could pay it off.</p>', unsafe_allow_html=True
)

# Inputs collected in the sidebar are recalculated whenever the user changes them.
st.sidebar.header("⚙️ Your loan")
loan_type = st.sidebar.selectbox(
    "What kind of loan?", ["Auto loan", "Student loan", "Personal loan", "Other loan"]
)
principal = st.sidebar.number_input(
    "Current loan balance ($)", min_value=100.0, max_value=1_000_000.0,
    value=25_000.0, step=500.0, format="%.2f"
)
apr = st.sidebar.number_input(
    "Fixed annual interest rate / APR (%)", min_value=0.0, max_value=40.0,
    value=6.5, step=0.25, format="%.2f"
)
years = st.sidebar.number_input(
    "Remaining loan term (years)", min_value=1, max_value=40, value=5, step=1
)
extra = st.sidebar.number_input(
    "Extra principal payment each month ($)", min_value=0.0, max_value=1_000_000.0,
    value=100.0, step=25.0, format="%.2f"
)
st.sidebar.caption("Adjust any input to recalculate your results instantly.")


def dollars(value: float) -> str:
    return f"${value:,.2f}"


def duration(months: int) -> str:
    yrs, remaining = divmod(months, 12)
    if yrs == 0:
        return f"{remaining} mo"
    if remaining == 0:
        return f"{yrs} yr" if yrs == 1 else f"{yrs} yrs"
    return f"{yrs} yr {remaining} mo" if yrs == 1 else f"{yrs} yrs {remaining} mo"


# Calculate the standard schedule and the schedule with extra principal payments.
try:
    normal = amortization_schedule(principal, apr, years, extra_payment=0.0)
    accelerated = amortization_schedule(principal, apr, years, extra_payment=extra)
except ValueError as error:
    st.error(f"Please check your input: {error}")
    st.stop()

interest_saved = max(0.0, normal["total_interest"] - accelerated["total_interest"])
months_saved = normal["months_to_payoff"] - accelerated["months_to_payoff"]
st.caption(f"{loan_type} · {dollars(principal)} balance · {apr:.2f}% APR · {years}-year term")

tab_results, tab_schedule, tab_education = st.tabs(
    ["📊 Your results", "📅 Payment schedule", "📖 Formula & assumptions"]
)

with tab_results:
    st.subheader("Your loan at a glance")
    a, b, c = st.columns(3)
    a.metric("Required monthly payment", dollars(normal["required_monthly_payment"]))
    b.metric("Interest without extra payments", dollars(normal["total_interest"]))
    c.metric("Original payoff time", duration(normal["months_to_payoff"]))
    st.divider()
    st.subheader("What if you pay extra?")
    a, b, c = st.columns(3)
    a.metric("Total interest saved", dollars(interest_saved))
    b.metric("Time saved", duration(months_saved))
    c.metric("New payoff time", duration(accelerated["months_to_payoff"]))
    if extra > 0:
        st.success(
            f"Paying **{dollars(extra)} extra each month** means a planned "
            f"payment of **{dollars(normal['required_monthly_payment'] + extra)}** "
            f"(until the smaller final payment). You could avoid "
            f"**{dollars(interest_saved)}** in interest."
        )
    else:
        st.info("Increase the extra payment in the sidebar to compare payoff options.")

    # Plot both balances, starting with the principal at Month 0.
    regular_by_month = {0: principal}
    regular_by_month.update({
        row["Month"]: row["Remaining Balance"] for row in normal["schedule"]
    })
    extra_by_month = {0: principal}
    extra_by_month.update({
        row["Month"]: row["Remaining Balance"] for row in accelerated["schedule"]
    })
    chart_data = pd.DataFrame({
        "Month": range(years * 12 + 1),
        "Minimum payments": [
            regular_by_month.get(i, 0.0) for i in range(years * 12 + 1)
        ],
        "With extra payments": [
            extra_by_month.get(i, 0.0) for i in range(years * 12 + 1)
        ],
    }).set_index("Month")
    st.subheader("Remaining loan balance over time")
    st.line_chart(chart_data)
    st.caption(
        "If the lines overlap, the extra payment is $0 or has no effect on payoff time."
    )

with tab_schedule:
    st.subheader("Month-by-month amortization")
    scenario = st.radio(
        "View schedule for", ["With extra payments", "Minimum payments only"],
        horizontal=True,
    )
    selected = accelerated if scenario == "With extra payments" else normal
    schedule_df = pd.DataFrame(selected["schedule"])
    currency_columns = ["Payment", "Principal", "Interest", "Remaining Balance"]
    currency_config = {
        column: st.column_config.NumberColumn(column, format="$%.2f")
        for column in currency_columns
    }
    st.dataframe(
        schedule_df, column_config=currency_config,
        use_container_width=True, hide_index=True
    )
    csv_bytes = schedule_df.round(2).to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download this schedule (CSV)", data=csv_bytes,
        file_name="payoffpath_amortization.csv", mime="text/csv"
    )
    st.caption("Monthly values are rounded to cents for display and export.")

with tab_education:
    st.subheader("How the math works")
    st.markdown("""
**Fixed monthly loan payment**

For a fixed-rate loan with monthly payments:

- P = starting loan balance
- r = annual APR / 100 / 12 (monthly interest rate)
- N = years × 12 (number of payments)

When r is greater than zero:

**Monthly payment = P × r / [1 − (1 + r)^(-N)]**

When r is zero, payment = P / N.

Each month, **interest = remaining balance × r**. The rest of the payment
reduces principal. Extra payments go to principal, potentially reducing the
loan term and total interest.

**Assumptions:** Fixed APR; payments at the end of every month; no origination
fees, late fees, taxes, insurance, prepayment penalties, or rate changes.
An actual lender may use daily interest accrual or different rounding rules.
""")
    st.markdown(
        "**Quick check:** A $12,000 loan at 0% APR for 3 years "
        "requires $333.33 per month before rounding."
    )
    st.caption("Educational tool only. This is not individualized financial advice.")

st.divider()
st.caption("Built using AI-assisted Python coding · Streamlit · Financial calculations")
