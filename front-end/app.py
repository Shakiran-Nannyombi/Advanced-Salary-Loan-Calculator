import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Salary & Loan Calculator",
    page_icon="💰",
    layout="wide"
)

# Constants
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def call_backend(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make API call to backend"""
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {str(e)}")
        return None

def display_amortization_schedule(schedule: list):
    """Display amortization schedule in a table"""
    if not schedule:
        return
    
    df = pd.DataFrame(schedule)
    df = df.round(2)  # Round all numbers to 2 decimal places
    
    # Format currency columns
    currency_columns = ['Payment', 'Principal', 'Interest', 'Remaining Balance']
    for col in currency_columns:
        df[col] = df[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df, use_container_width=True)

# Main app
st.title("💰 Salary & Loan Calculator")

# Create tabs for different calculators
tab1, tab2 = st.tabs(["Salary Advance Calculator", "Loan Calculator"])

# Salary Advance Calculator Tab
with tab1:
    st.header("Salary Advance Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gross_salary = st.number_input(
            "Gross Salary",
            min_value=0.0,
            step=1000.0,
            help="Enter your gross salary"
        )
        
        pay_frequency = st.selectbox(
            "Pay Frequency",
            options=["monthly", "biweekly", "weekly"],
            help="Select how often you get paid"
        )
    
    with col2:
        requested_amount = st.number_input(
            "Requested Advance Amount",
            min_value=0.0,
            step=100.0,
            help="Enter the amount you want to advance"
        )
    
    if st.button("Calculate Advance", key="advance"):
        if gross_salary and requested_amount:
            data = {
                "gross_salary": gross_salary,
                "pay_frequency": pay_frequency,
                "requested_amount": requested_amount
            }
            
            result = call_backend("calculate_advance", data)
            
            if result:
                st.success("Advance Calculation Complete!")
                
                # Display results in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Maximum Advance", f"${result['max_advance']:,.2f}")
                
                with col2:
                    st.metric("Approved Amount", f"${result['approved_amount']:,.2f}")
                
                with col3:
                    st.metric("Fee", f"${result['fee']:,.2f}")
                
                st.metric("Total Repayable", f"${result['total_repayable']:,.2f}")

# Loan Calculator Tab
with tab2:
    st.header("Loan Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0.0,
            step=1000.0,
            help="Enter the loan amount"
        )
        
        interest_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            help="Enter the annual interest rate"
        )
    
    with col2:
        loan_term = st.number_input(
            "Loan Term (months)",
            min_value=1,
            max_value=360,
            step=1,
            help="Enter the loan term in months"
        )
    
    if st.button("Calculate Loan", key="loan"):
        if loan_amount and interest_rate and loan_term:
            data = {
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term_months": loan_term
            }
            
            result = call_backend("calculate_loan", data)
            
            if result:
                st.success("Loan Calculation Complete!")
                
                # Display summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Monthly Payment", f"${result['monthly_payment']:,.2f}")
                
                with col2:
                    st.metric("Total Interest", f"${result['total_interest']:,.2f}")
                
                with col3:
                    st.metric("Total Payment", f"${result['total_payment']:,.2f}")
                
                # Display amortization schedule
                st.subheader("Amortization Schedule")
                display_amortization_schedule(result['amortization_schedule']) 