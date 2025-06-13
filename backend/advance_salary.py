from fastapi import APIRouter
from models import SalaryAdvanceRequest, SalaryAdvanceResponse

router = APIRouter()

# Constants
MAX_ADVANCE_PERCENTAGE = 0.5  # 50% of monthly salary
ADVANCE_FEE_PERCENTAGE = 0.02  # 2% fee

# function to convert salary to monthly amount based on pay frequency
def convert_to_monthly(salary: float, frequency: str) -> float:
    conversion_rates = {
        "monthly": 1,
        "biweekly": 26 / 12,
        "weekly": 52 / 12
    } 
    return salary * conversion_rates[frequency.lower()]

@router.post("/calculate_salary_advance", response_model=SalaryAdvanceResponse)
def calculate_advance(request: SalaryAdvanceRequest):

    # Calculate monthly salary based on pay frequency
    monthly_salary = convert_to_monthly(request.gross_salary, request.pay_frequency)
    max_advance = monthly_salary * MAX_ADVANCE_PERCENTAGE

    # Checking if the requested amount is eligible for advance
    is_eligible = request.requested_amount <= max_advance
    fee = request.requested_amount * ADVANCE_FEE_PERCENTAGE if is_eligible else 0
    total_repayable = request.requested_amount + fee if is_eligible else 0

    return SalaryAdvanceResponse(
        eligible=is_eligible,
        max_advance=round(max_advance, 2),
        approved_amount=round(request.requested_amount, 2) if is_eligible else 0,
        fee=round(fee, 2),
        total_repayable=round(total_repayable, 2),
        monthly_salary=round(monthly_salary, 2)
    )
