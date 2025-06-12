from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from models import SalaryAdvanceRequest, LoanRequest

app = FastAPI(title="Salary Loan Calculator API")

# Calculate salary advance endpoint
@app.post("/calculate_advance")
async def calculate_advance(request: SalaryAdvanceRequest):
    try:
        # Convert salary to monthly if needed
        monthly_salary = convert_to_monthly(request.gross_salary, request.pay_frequency)
        
        # Basic eligibility check (e.g., advance can't exceed 50% of monthly salary)
        max_advance = monthly_salary * 0.5
        
        if request.requested_amount > max_advance:
            raise HTTPException(
                status_code=400,
                detail=f"Requested amount exceeds maximum allowed advance of {max_advance:.2f}"
            )
        
        # Calculate fees (example: 2% of advance amount)
        fee = request.requested_amount * 0.02
        total_repayable = request.requested_amount + fee
        
        return {
            "eligible": True,
            "max_advance": max_advance,
            "approved_amount": request.requested_amount,
            "fee": fee,
            "total_repayable": total_repayable
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Calculate loan endpoint
@app.post("/calculate_loan")
async def calculate_loan(request: LoanRequest):
    try:
        # Convert annual interest rate to monthly
        monthly_rate = request.interest_rate / 100 / 12
        
        # Calculate monthly payment using the loan amortization formula
        monthly_payment = calculate_monthly_payment(
            request.loan_amount,
            monthly_rate,
            request.loan_term_months
        )
        
        # Generate amortization schedule
        schedule = generate_amortization_schedule(
            request.loan_amount,
            monthly_rate,
            request.loan_term_months,
            monthly_payment
        )
        
        return {
            "monthly_payment": monthly_payment,
            "total_interest": schedule["total_interest"],
            "total_payment": schedule["total_payment"],
            "amortization_schedule": schedule["schedule"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
def convert_to_monthly(salary: float, frequency: str) -> float:
    """Convert salary to monthly amount based on pay frequency."""
    if frequency.lower() == "monthly":
        return salary
    elif frequency.lower() == "biweekly":
        return salary * 26 / 12
    elif frequency.lower() == "weekly":
        return salary * 52 / 12
    else:
        raise ValueError("Invalid pay frequency")

def calculate_monthly_payment(principal: float, monthly_rate: float, term_months: int) -> float:
    """Calculate monthly payment using the loan amortization formula."""
    if monthly_rate == 0:
        return principal / term_months
    
    return principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)

def generate_amortization_schedule(principal: float, monthly_rate: float, term_months: int, monthly_payment: float) -> dict:
    """Generate loan amortization schedule using pandas."""
    # Create arrays for the schedule
    periods = np.arange(1, term_months + 1)
    remaining_balance = np.zeros(term_months)
    interest_payment = np.zeros(term_months)
    principal_payment = np.zeros(term_months)
    
    # Calculate for each period
    remaining_balance[0] = principal
    for i in range(term_months):
        interest_payment[i] = remaining_balance[i] * monthly_rate
        principal_payment[i] = monthly_payment - interest_payment[i]
        if i < term_months - 1:
            remaining_balance[i + 1] = remaining_balance[i] - principal_payment[i]
    
    # Create DataFrame
    schedule_df = pd.DataFrame({
        'Period': periods,
        'Payment': monthly_payment,
        'Principal': principal_payment,
        'Interest': interest_payment,
        'Remaining Balance': remaining_balance
    })
    
    return {
        "schedule": schedule_df.to_dict(orient='records'),
        "total_interest": interest_payment.sum(),
        "total_payment": monthly_payment * term_months
    } 