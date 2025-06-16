from pydantic import BaseModel, EmailStr, Field

class SalaryAdvanceRequest(BaseModel):
    gross_salary: float
    pay_frequency: str  # monthly, biweekly, weekly
    requested_amount: float

class SalaryAdvanceResponse(BaseModel):
    eligible: bool
    max_advance: float
    approved_amount: float
    fee: float
    total_repayable: float
    monthly_salary: float

class LoanRequest(BaseModel):
    loan_amount: float
    interest_rate: float
    loan_term_months: int 

class LoanResponse(BaseModel):
    monthly_payment: float
    total_interest: float
    total_payment: float

class PaymentScheduleRequest(BaseModel):
    principal: float
    monthly_rate: float
    term_months: int
    monthly_payment: float

class PaymentScheduleResponse(BaseModel):
    schedule: list[dict]
    total_interest: float
    total_payment: float

class CustomerInfo(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    employment_status: str = Field(..., min_length=1, max_length=50)
    employee_id: str | None = None
    company_name: str | None = None
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)

class CustomerResponse(BaseModel):
    message: str

class CustomerData(BaseModel):
    full_name: str
    employment_status: str
    employee_id: str
    company_name: str
    email: EmailStr
    phone_number: str

class CustomerDataResponse(BaseModel):
    customer_data: CustomerData | None = None
    message: str

class LoanApplicationRequest(BaseModel):
    house_ownership: str
    salary_deduction_approval: str
    dependents: int
    employment_duration: str
    payment_schedule_csv: str # This will hold the base64 encoded CSV string

class LoanApplicationResponse(BaseModel):
    message: str
