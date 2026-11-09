# 💸 PayoffPath — Loan Payoff Planner

PayoffPath is a beginner-friendly **Streamlit finance web app** built with AI-assisted coding. It helps users understand fixed-rate loans and the financial effect of making extra principal payments.

## Problem solved
Borrowers may know their monthly payment but not their total lifetime interest expense. PayoffPath calculates both and compares the standard payoff schedule with an accelerated schedule.

## Features
- Choose loan type and enter balance, fixed annual APR, remaining loan years, and extra monthly principal payment
- Calculate monthly payment, total interest, and payoff period
- Show interest savings and time saved from extra payments
- Plot both remaining loan balances in an interactive chart
- View a month-by-month amortization schedule and download CSV
- Review formulas, assumptions, and input validation

## Project files
- `app.py`: Streamlit interface and chart
- `calculator.py`: Loan formulas and amortization logic
- `requirements.txt`: Python package requirements
- `test_calculator.py`: Verification tests for math and edge cases
- `AI_PROMPT_AND_TESTING.md`: Prompt, explanation, and test documentation

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
To run tests:
```bash
python -m unittest test_calculator.py -v
```

## Deploy with Streamlit Community Cloud
1. Keep these files in the root of this public GitHub repository.
2. Open https://share.streamlit.io and sign in with GitHub.
3. Create an app from repository `jcope27/payoff-loan-planner`.
4. Choose branch `main` and main file path `app.py`; deploy.
5. Verify the live app, then submit **its publicly accessible `.streamlit.app` URL** to Canvas.

## Financial formulas
For principal P, monthly rate r = APR / 100 / 12, and N = years × 12:

**Monthly payment = P × r / [1 − (1 + r)^(-N)]**

If r = 0, the payment is P / N. Each month, interest equals outstanding balance × r; the payment minus interest reduces the principal. Any extra payment goes toward principal. The final payment is capped to avoid overpayment.

## Limitations
This is an educational simulation, not a lending quote. It assumes fixed interest with monthly payments in arrears and excludes fees, taxes, insurance, penalties, and daily interest accrual. Actual lender schedules may vary.
