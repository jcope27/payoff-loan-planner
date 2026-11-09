"""Financial calculations for PayoffPath. Fixed APR; monthly payments in arrears."""
from math import isfinite


def monthly_payment(principal: float, annual_rate_percent: float, years: int) -> float:
    """Return the standard fully amortizing monthly payment."""
    _validate(principal, annual_rate_percent, years, 0.0)
    months = years * 12
    r = annual_rate_percent / 100 / 12
    if r == 0:
        return principal / months
    return principal * r / (1 - (1 + r) ** (-months))


def _validate(principal: float, annual_rate_percent: float, years: int, extra: float) -> None:
    """Reject inputs that would make an invalid loan schedule."""
    for name, value in (
        ("Loan amount", principal), ("APR", annual_rate_percent), ("Extra payment", extra)
    ):
        if not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{name} must be a finite number.")
    if principal <= 0:
        raise ValueError("Loan amount must be greater than $0.")
    if not 0 <= annual_rate_percent <= 40:
        raise ValueError("APR must be between 0% and 40%.")
    if isinstance(years, bool) or not isinstance(years, int) or not 1 <= years <= 40:
        raise ValueError("Loan term must be a whole number from 1 to 40 years.")
    if extra < 0:
        raise ValueError("Extra payment cannot be negative.")


def amortization_schedule(
    principal: float, annual_rate_percent: float, years: int, extra_payment: float = 0.0
) -> dict:
    """Calculate monthly interest, principal, balances, and payoff statistics."""
    _validate(principal, annual_rate_percent, years, extra_payment)
    required_payment = monthly_payment(principal, annual_rate_percent, years)
    monthly_rate = annual_rate_percent / 100 / 12
    balance = float(principal)
    total_interest = 0.0
    total_paid = 0.0
    schedule = []
    for month in range(1, years * 12 + 1):
        interest = balance * monthly_rate
        payment = min(required_payment + extra_payment, balance + interest)
        principal_paid = payment - interest
        balance = max(0.0, balance - principal_paid)
        if balance < max(1e-9, principal * 1e-12):
            balance = 0.0
        total_interest += interest
        total_paid += payment
        schedule.append({
            "Month": month,
            "Payment": payment,
            "Principal": principal_paid,
            "Interest": interest,
            "Remaining Balance": balance,
        })
        if balance == 0:
            break
    return {
        "required_monthly_payment": required_payment,
        "total_interest": total_interest,
        "total_paid": total_paid,
        "months_to_payoff": len(schedule),
        "schedule": schedule,
    }
