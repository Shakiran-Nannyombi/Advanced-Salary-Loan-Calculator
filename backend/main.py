from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from advance_salary import router as salary_router
from customer_info import router as customer_router
from loan_calculation import router as loan_router
from payment_schedule import router as payment_router

app = FastAPI(title="Salary Advance Calculator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(salary_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(loan_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Salary Advance Calculator API"}