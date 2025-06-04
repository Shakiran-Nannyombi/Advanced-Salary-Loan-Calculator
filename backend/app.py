from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoanRequest(BaseModel):
    gross_pay: float
    loan_amount: float
    loan_duration: int
    variable_interest_rate: float

class LoanResponse(BaseModel):
    eligible: bool
    monthly_payment: float = 0.0
    total_payment_with_interest: float = 0.0

@app.post("/calculate-loan", response_model=LoanResponse)
def calculate_loan(data: LoanRequest):
    # checking eligibility
    if data.gross_pay > 0 and data.loan_duration > 0:
        max_loan = data.gross_pay * 0.6
        eligible = data.loan_amount <= max_loan and data.loan_amount > 0
    
    if not eligible:
        return LoanResponse(eligible=False)
    
    # Calculating monthly interest rate
    monthly_interest_rate = data.variable_interest_rate / 100 / 12

    # Calculating monthly payment using amortization formula
    if monthly_interest_rate > 0:
        numerator = data.loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** data.loan_duration
        denominator = (1 + monthly_interest_rate) ** data.loan_duration - 1
        monthly_payment = numerator / denominator
    else:
        monthly_payment = data.loan_amount / data.loan_duration

    total_payment_with_interest = monthly_payment * data.loan_duration

    return LoanResponse(
        eligible=True,
        monthly_payment=round(monthly_payment, 2),
        total_payment_with_interest=round(total_payment_with_interest, 2),
    )

@app.post("/loan-analysis")
def loan_analysis(data: LoanRequest):
    analysis_data = {
        "loan_amount": data.loan_amount,
        "loan_duration": data.loan_duration,
        "variable_interest_rate": data.variable_interest_rate,
        "eligible": data.loan_amount <= (data.gross_pay * 0.6) and data.loan_amount > 0,
    }
    
    return analysis_data