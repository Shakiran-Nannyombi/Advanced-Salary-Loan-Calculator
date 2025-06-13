from fastapi import APIRouter, HTTPException
import json
import os
from models import CustomerInfo, CustomerResponse

router = APIRouter()

# File path for storing customer data
DATA_FILE = "/data/customer_data.json"

# Functions to load and read customer data from a JSON file
def load_customer_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading customer data: {e}")
        return {}

# Function to save customer data to a JSON file
def save_customer_data(data):
    try:
        # Checking if the directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving customer data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save customer data: {str(e)}")

@router.post("/save-customer")
def save_customer_info(customer: CustomerInfo):
    try:
        # Load existing data
        customer_data = load_customer_data()
        
        # Convert customer model to dict
        customer_dict = customer.model_dump()
        
        # Update with new customer info
        customer_data[customer.email] = customer_dict
        
        # Save updated data
        save_customer_data(customer_data)
        
        return CustomerResponse(message=f"Customer information saved successfully for {customer.full_name}")
    except Exception as e:
        print(f"Error in save_customer_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-customer/{email}")
async def get_customer_info(email: str):
    """Retrieve customer information by email."""
    try:
        customer_data = load_customer_data()
        if email not in customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer_data[email]
    except Exception as e:
        print(f"Error in get_customer_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
