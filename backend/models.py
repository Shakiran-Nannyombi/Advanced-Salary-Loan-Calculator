from pydantic import BaseModel

class SalaryAdvanceRequest(BaseModel):
    gross_salary: float
    pay_frequency: str  # monthly, biweekly, weekly
    requested_amount: float

class LoanRequest(BaseModel):
    loan_amount: float
    interest_rate: float
    loan_term_months: int 