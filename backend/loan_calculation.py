from fastapi import APIRouter
from models import LoanRequest, LoanResponse


router = APIRouter()

# function for calculating monthly payment using the loan amortization formula
def calculate_monthly_payment(principal: float, monthly_rate: float, term_months: int) -> float:
    if monthly_rate == 0:
        return principal / term_months #to give a false answer if the interest rate is 0
    else:
        return principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)


@router.post("/calculate_loan", response_model=LoanResponse)
def calculate_loan(request: LoanRequest):
    loan_amount = request.loan_amount
    interest_rate = request.interest_rate
    loan_term_months = request.loan_term_months

    # Calculate monthly payment 
    monthly_rate = interest_rate / 100 / 12
    monthly_payment = calculate_monthly_payment(
        loan_amount,
        monthly_rate,
        loan_term_months
    )

    return LoanResponse(
        monthly_payment=round(monthly_payment, 2),
        total_interest=round((monthly_payment * loan_term_months) - loan_amount, 2),
        total_payment=round(monthly_payment * loan_term_months, 2)
    )
