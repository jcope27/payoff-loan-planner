# AI-Assisted Development and Verification

## CRAFT prompt

**Context:** Finance coursework requires a publicly deployed web app made with AI-assisted coding, Python, GitHub, and Streamlit.

**Role:** Act as a careful finance software developer and a beginner-friendly coding tutor.

**Action:** Build a fixed-rate loan payoff app that calculates monthly payments, total interest, and the effect of optional extra monthly principal payments.

**Format:** Provide commented Python files, package requirements, a README, unit tests, and a clear interface with user inputs, a chart, payoff comparisons, a monthly schedule, and CSV download. Validate inputs and explain the formulas.

**Tone:** Professional, simple, and accessible to beginners.

## Code explanation
- `calculator.py` checks numerical inputs, calculates the monthly payment, and loops through each month to allocate payments between interest and principal.
- `app.py` creates user controls, displays results and charts, and exports the schedule as a CSV.
- `requirements.txt` lists the packages Streamlit Cloud installs.
- `test_calculator.py` verifies correctness and catches invalid inputs.

## Independent math checks
- A $12,000 loan at 0% for 3 years requires $12,000 ÷ 36 = **$333.33 per month** (display rounded); interest = **$0**.
- A $200,000 fixed-rate loan at 6% over 30 years has a monthly payment of approximately **$1,199.10**.
- Adding extra principal must not increase total interest or payoff time, and the final balance should be zero.
- The final loan payment is capped at the outstanding balance plus that month's interest.

## Automated verification performed
All eight local Python unit tests passed on November 9, 2026:
1. Fixed-rate benchmark payment — PASS
2. Zero-interest payment — PASS
3. Extra payment saves time and interest — PASS
4. No-extra case equals baseline — PASS
5. Very large extra payment ends loan in one month — PASS
6. Final balance zero without overpayment — PASS
7. Invalid input rejection (11 cases) — PASS
8. Large loan is finite and fully paid — PASS

The live deployed Streamlit website has **not** yet been tested.

## Live deployment checklist (complete after publishing)
- [ ] Change loan balance, APR, term, and extra payment; results update.
- [ ] Set APR to 0%; no divide-by-zero error and total interest $0.
- [ ] Set extra payment to $0; interest/time savings become $0.
- [ ] Set a very large extra payment; loan pays off in one month.
- [ ] Open the schedule and verify its last remaining balance is $0.
- [ ] Download CSV and verify rows and headers.
- [ ] Open the public URL in another browser/device.

## Potential improvements
Add loan dates, variable rates, fees, one-time extra payments, and saved scenarios. These were left out to keep this version understandable and testable.
