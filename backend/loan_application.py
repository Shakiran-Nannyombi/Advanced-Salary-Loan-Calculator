from fastapi import APIRouter, HTTPException
from models import LoanApplicationRequest, LoanApplicationResponse
import base64
import pandas as pd
import io

router = APIRouter()

@router.post("/submit_loan_application", response_model=LoanApplicationResponse)
async def submit_loan_application(request: LoanApplicationRequest):
    try:
        # Decode the base64 CSV string
        csv_bytes = base64.b64decode(request.payment_schedule_csv)
        csv_file = io.StringIO(csv_bytes.decode('utf-8'))
        
        # Read the CSV into a pandas DataFrame (optional, for validation/processing)
        payment_schedule_df = pd.read_csv(csv_file)
        
        # Here you would typically save the loan application details and the payment schedule
        # to a database or perform further processing.
        # For now, we'll just log the receipt and return a success message.
        
        print(f"Loan Application Received for: House Ownership - {request.house_ownership}, "
              f"Salary Deduction Approval - {request.salary_deduction_approval}, "
              f"Dependents - {request.dependents}, "
              f"Employment Duration - {request.employment_duration}")
        print("Payment Schedule (first 5 rows):\n", payment_schedule_df.head().to_string())

        return LoanApplicationResponse(message="Loan application submitted successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit loan application: {str(e)}") 