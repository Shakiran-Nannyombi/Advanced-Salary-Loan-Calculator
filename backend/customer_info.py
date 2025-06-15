import json
import os
import logging
from fastapi import APIRouter, HTTPException
from filelock import FileLock
from .models import CustomerInfo, CustomerResponse

router = APIRouter()
DATA_FILE = "data/customer_data.json"
LOCK_FILE = DATA_FILE + ".lock"

# Set up logging to prevent issues with file access
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_customer_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {}
        with FileLock(LOCK_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading customer data: {e}")
        return {}

def save_customer_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with FileLock(LOCK_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving customer data: {e}")
        raise HTTPException(status_code=500, detail="Failed to save customer data.")

@router.post("/save-customer", response_model=CustomerResponse)
def save_customer(customer: CustomerInfo):
    data = load_customer_data()
    if customer.email in data:
        logger.warning(f"Attempt to overwrite existing customer: {customer.email}")
        raise HTTPException(status_code=400, detail="Customer with this email already exists.")
    data[customer.email] = customer.model_dump()
    save_customer_data(data)
    logger.info(f"Customer saved: {customer.email}")
    return CustomerResponse(message="Customer information saved successfully.")

@router.get("/get-customer/{email}", response_model=CustomerInfo)
def get_customer(email: str):
    data = load_customer_data()
    if email not in data:
        logger.warning(f"Customer not found: {email}")
        raise HTTPException(status_code=404, detail="Customer not found.")
    logger.info(f"Customer retrieved: {email}")
    return CustomerInfo(**data[email])
