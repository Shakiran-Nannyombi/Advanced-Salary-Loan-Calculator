from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class LoanRequest(BaseModel):
    gross_pay: float
    loan_amount: float
    loan_duration: int
    variable_interest_rate: float


class AdvanceRequest(BaseModel):
    gross_pay: float
    advance_amount: float
    advance_duration: int
    variable_interest_rate: float


class AdvanceResponse(BaseModel):
    eligible: bool
    max_advance_amount: float = 0.0


class LoanResponse(BaseModel):
    eligible: bool
    monthly_payment: float = 0.0
    total_payment_with_interest: float = 0.0


class LoanAnalysisRequest(BaseModel):
    gross_pay: float
    loan_amount: float
    loan_duration: int
    variable_interest_rate: float
    eligible: bool = False
    monthly_payment: float = 0.0
    total_payment_with_interest: float = 0.0


@app.post("/calculate-advance", response_model=AdvanceResponse)
def calculate_advance(data: AdvanceRequest):
    max_advance = data.gross_pay * 0.4
    eligible = (data.advance_amount <= max_advance and 
               data.advance_amount > 0 and 
               data.gross_pay > 0)
    return AdvanceResponse(eligible=eligible, max_advance_amount=max_advance)


@app.post("/calculate-loan", response_model=LoanResponse)
def calculate_loan(data: LoanRequest):
    monthly_interest_rate = data.variable_interest_rate / 100 / 12

    if monthly_interest_rate > 0:
        numerator = (
            data.loan_amount
            * monthly_interest_rate
            * (1 + monthly_interest_rate) ** data.loan_duration
        )
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
def loan_analysis(data: LoanAnalysisRequest):
    analysis_data = {
        "gross_pay": data.gross_pay,
        "loan_amount": data.loan_amount,
        "loan_duration": data.loan_duration,
        "variable_interest_rate": data.variable_interest_rate,
        "eligible": data.eligible,
        "monthly_payment": data.monthly_payment,
        "total_payment_with_interest": data.total_payment_with_interest,
    }
    return analysis_data
