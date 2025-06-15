from fastapi import APIRouter, HTTPException
from models import PaymentScheduleRequest, PaymentScheduleResponse
import numpy as np
import pandas as pd


router = APIRouter()

@router.post("/generate_payment_schedule", response_model=PaymentScheduleResponse)
def generate_payment_schedule(request: PaymentScheduleRequest):
    principal = request.principal
    monthly_rate = request.monthly_rate
    term_months = request.term_months
    monthly_payment = request.monthly_payment

    # Edge Case: Prevent negative amortization
    min_payment = principal * monthly_rate
    if monthly_rate > 0 and monthly_payment <= min_payment:
        raise HTTPException(
            status_code=400,
            detail="Monthly payment is too low to cover the interest. Balance will never reach zero."
        )

    # Efficient array operations with NumPy for performance
    periods = np.arange(1, term_months + 1)
    remaining_balance = np.zeros(term_months + 1)
    interest_payment = np.zeros(term_months)
    principal_payment = np.zeros(term_months)

    remaining_balance[0] = principal

    for i in range(term_months):
        # Calculate interest and principal, rounding for consistency
        interest_payment[i] = round(remaining_balance[i] * monthly_rate, 2)
        principal_payment[i] = round(monthly_payment - interest_payment[i], 2)
        if i < term_months - 1:
            remaining_balance[i + 1] = round(remaining_balance[i] - principal_payment[i], 2)

    # Rounding for display and calculations is now consistent
    df = pd.DataFrame({
        "Period": periods,
        "Payment": np.round([monthly_payment] * term_months, 2),
        "Principal": principal_payment,
        "Interest": interest_payment,
        "Remaining Balance": np.round(remaining_balance[1:], 2)
    })

    total_interest = float(np.round(np.sum(interest_payment), 2))
    total_payment = float(np.round(monthly_payment * term_months, 2))

    return PaymentScheduleResponse(
        schedule=df.to_dict(orient="records"),
        total_interest=total_interest,
        total_payment=total_payment
    )