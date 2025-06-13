import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Salary Loan Calculator",
    page_icon="💰",
    layout="wide",
)

# UI Header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=100)
    st.title("Advance Salary Loan Calculator")

st.divider()

# Customer Information Form
st.subheader("Customer Information")
with st.form("customer_info"):
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("FULL NAME", placeholder="Enter your full name")
        employment_status = st.selectbox("EMPLOYMENT STATUS", 
            options=["Employed", "Self-Employed", "Unemployed"])
        employee_id = st.text_input("EMPLOYEE ID", placeholder="Enter your employee ID")
    with col2:
        company_name = st.text_input("COMPANY NAME", placeholder="Enter your company name")
        email = st.text_input("EMAIL", placeholder="Enter your email address")
        phone_number = st.text_input("PHONE NUMBER", placeholder="Enter your phone number")
    
    customer_submit = st.form_submit_button("Save Customer Information")

if customer_submit and full_name and email and phone_number:
    try:
        response = requests.post(
            "http://backend:8000/customer/save-customer",
            json={
                "full_name": full_name,
                "employment_status": employment_status,
                "employee_id": employee_id if employee_id else None,
                "company_name": company_name if company_name else None,
                "email": email,
                "phone_number": phone_number
            }
        )
        if response.ok:
            st.success(response.json()["message"])
    except Exception as e:
        st.error(f"Error saving customer information: {str(e)}")

# Calculator Selection
st.subheader("Select Calculator Type")
tab1, tab2 = st.tabs(["Salary Advance Calculator", "Loan Calculator"])

# Salary Advance Calculator
with tab1:
    st.header("Salary Advance Calculator")
    with st.form("advance_calculator"):
        col1, col2 = st.columns(2)
        with col1:
            gross_salary = st.number_input("GROSS SALARY", min_value=0.0, step=1000.0)
            pay_frequency = st.selectbox("PAY FREQUENCY", options=["monthly", "biweekly", "weekly"])
        with col2:
            requested_amount = st.number_input("REQUESTED ADVANCE AMOUNT", min_value=0.0, step=100.0)
        
        submit = st.form_submit_button("Calculate Advance")

    if submit and gross_salary and requested_amount:
        try:
            response = requests.post(
                "http://backend:8000/advance/calculate_salary_advance",
                json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency,
                    "requested_amount": requested_amount
                }
            )
            if response.ok:
                result = response.json()
                if result['eligible']:
                    st.success(f"✅ {full_name}, you are eligible for an advance!")
                    st.info("Calculation Results")
                    cols = st.columns(4)
                    with cols[0]: st.metric("Maximum Advance", f"${result['max_advance']:,.2f}")
                    with cols[1]: st.metric("Approved Amount", f"${result['approved_amount']:,.2f}")
                    with cols[2]: st.metric("Fee", f"${result['fee']:,.2f}")
                    with cols[3]: st.metric("Total Repayable", f"${result['total_repayable']:,.2f}")
                else:
                    st.warning(f"⚠️ {full_name}, your requested amount (${requested_amount:,.2f}) exceeds the maximum advance available (${result['max_advance']:,.2f})")
        except Exception as e:
            st.error(f"Error calculating advance: {str(e)}")

# Loan Calculator
with tab2:
    st.header("Loan Calculator")
    with st.form("loan_calculator"):
        col1, col2 = st.columns(2)
        with col1:
            loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
            interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
        with col2:
            loan_term = st.number_input("Loan Term (months)", min_value=1, max_value=360, step=1)
        
        submit = st.form_submit_button("Calculate Loan")

    if submit and loan_amount and interest_rate and loan_term:
        try:
            response = requests.post(
                "http://backend:8000/loan/calculate_loan",
                json={
                    "loan_amount": loan_amount,
                    "interest_rate": interest_rate,
                    "loan_term_months": loan_term
                }
            )
            if response.ok:
                result = response.json()
                st.success(f"{full_name}, your loan calculation is complete!")
                st.info("Calculation Results")
                cols = st.columns(3)
                with cols[0]: st.metric("Monthly Payment", f"${result['monthly_payment']:,.2f}")
                with cols[1]: st.metric("Total Interest", f"${result['total_interest']:,.2f}")
                with cols[2]: st.metric("Total Payment", f"${result['total_payment']:,.2f}")
                
                # Get payment schedule
                schedule_response = requests.post(
                    "http://backend:8000/payment/generate_payment_schedule",
                    json={
                        "principal": loan_amount,
                        "monthly_rate": interest_rate / 100 / 12,
                        "term_months": loan_term,
                        "monthly_payment": result['monthly_payment']
                    }
                )
                if schedule_response.ok:
                    schedule = schedule_response.json()
                    st.subheader("Payment Schedule")
                    df = pd.DataFrame(schedule['schedule'])
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Payment Schedule",
                        data=csv,
                        file_name='payment_schedule.csv',
                        mime='text/csv'
                    )
        except Exception as e:
            st.error(f"Error calculating loan: {str(e)}")