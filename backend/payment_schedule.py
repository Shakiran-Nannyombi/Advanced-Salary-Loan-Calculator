from fastapi import APIRouter
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

    # Generate payment schedule
    periods = np.arange(1, term_months + 1)
    remaining_balance = np.zeros(term_months)
    interest_payment = np.zeros(term_months)
    principal_payment = np.zeros(term_months)

    remaining_balance[0] = principal
    for i in range(term_months):
        interest_payment[i] = remaining_balance[i] * monthly_rate
        principal_payment[i] = monthly_payment - interest_payment[i]
        if i < term_months - 1:
            remaining_balance[i + 1] = remaining_balance[i] - principal_payment[i]

    schedule_df = pd.DataFrame({
        'Period': periods,
        'Payment': np.round(monthly_payment, 2),
        'Principal': np.round(principal_payment, 2),
        'Interest': np.round(interest_payment, 2),
        'Remaining Balance': np.round(remaining_balance, 2)
    })

    return PaymentScheduleResponse(
        schedule=schedule_df.to_dict(orient='records'),
        total_interest=float(np.round(interest_payment.sum(), 2)),
        total_payment=float(np.round(monthly_payment * term_months, 2))
    )