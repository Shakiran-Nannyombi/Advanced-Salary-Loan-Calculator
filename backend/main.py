from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from salary_advance import router as salary_router
from customer_info import router as customer_router

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

@app.get("/")
async def root():
    return {"message": "Welcome to Salary Advance Calculator API"}