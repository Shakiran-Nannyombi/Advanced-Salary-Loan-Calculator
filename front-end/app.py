import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Salary Loan Calculator",
    page_icon="💰",
    layout="wide",
)

# Page Header
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
        st.markdown("<div style='color: gray;'>Note: If you are employed, please provide your employee ID and company name.</div>", unsafe_allow_html=True)
        employee_id = st.text_input("EMPLOYEE ID", placeholder="Enter your employee ID")

    with col2:
        company_name = st.text_input("COMPANY NAME", placeholder="Enter your company name")
        email = st.text_input("EMAIL", placeholder="Enter your email address")
        phone_number = st.text_input("PHONE NUMBER", placeholder="Enter your phone number")
    
    customer_submit = st.form_submit_button("Save Customer Information")

if customer_submit:
    # Check if any required field is empty
    if not all([full_name, email, phone_number]) or (employment_status == "Employed" and not all([company_name, employee_id])):
        st.error("Please fill in all required fields. No empty fields are allowed.")
    else:
        try:
            response = requests.post(
                "http://backend:8000/api/v1/save-customer",
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
tab1, tab2 ,tab3= st.tabs(["Salary Advance Calculator", "Loan Calculator","Loan Application Form"])

# Salary Advance Calculator
with tab1:
    st.header("Salary Advance Calculator")
    st.write("Use this calculator to determine your eligibility for a salary advance and the maximum amount you can request.")
    
    with st.form("advance_calculator"):
        col1, col2 = st.columns(2)

        with col1:
            gross_salary = st.number_input("GROSS SALARY", min_value=0.0, step=1000.0)
            st.markdown("<div style='color: gray;'>Gross salary is your total earnings before deductions.</div>", unsafe_allow_html=True)
            pay_frequency = st.selectbox("PAY FREQUENCY", options=["monthly", "biweekly", "weekly"])
            st.markdown("<div style='color: gray;'>Pay frequency determines how often you are paid.</div>", unsafe_allow_html=True)
        
        with col2:
            requested_amount = st.number_input("REQUESTED ADVANCE AMOUNT", min_value=0.0, step=100.0)
            st.markdown("<div style='color: gray;'>Requested amount will determine your eligibility for an advance.</div>", unsafe_allow_html=True)
            st.markdown("<div style='color: gray;'>Note: Ensure the requested amount is not more than half of your gross salary.</div>", unsafe_allow_html=True)
            st.write("Please ensure all fields are filled out correctly before submitting.")
        
        submit = st.form_submit_button("Calculate Advance")

    if submit and gross_salary and requested_amount:
        try:
            response = requests.post(
                "http://backend:8000/api/v1/calculate_salary_advance",
                json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency,
                    "requested_amount": requested_amount
                }
            )
            if response.ok:
                result = response.json()
                if result['eligible']:
                    st.success(f"Congratulations {full_name}, you are eligible for an advance!")
                    st.info("Calculation Results")
                    cols = st.columns(4)
                    with cols[0]: st.metric("Maximum Advance", f"${result['max_advance']:,.2f}")
                    with cols[1]: st.metric("Approved Amount", f"${result['approved_amount']:,.2f}")
                    with cols[2]: st.metric("Fee", f"${result['fee']:,.2f}")
                    with cols[3]: st.metric("Total Repayable", f"${result['total_repayable']:,.2f}")
                    st.write("You can proceed to request the advance amount in the loan application form.")
                else:
                    st.warning(f"⚠️ Apologies {full_name}, your requested amount ${requested_amount:,.2f} exceeds the maximum advance available.")
                    st.warning(f"Maximum Advance Available: ${result['max_advance']:,.2f}")
        except Exception as e:
            st.error(f"Error calculating advance: {str(e)}")

# Loan Calculator
with tab2:
    st.header("Loan Calculator")
    st.write("Use this calculator to determine your monthly payments, total interest, and total payment for a loan.")
    
    with st.form("loan_calculator"):
        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
            interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
            st.markdown("<div style='color: gray;'>Note: Interest rate is yearly.</div>", unsafe_allow_html=True)
        
        with col2:
            loan_term = st.number_input("Loan Term (months)", min_value=1, max_value=360, step=1)
            st.markdown("<div style='color: gray;'>Note: Loan term is in months.</div>", unsafe_allow_html=True)
            st.write("Please ensure all fields are filled out correctly before submitting.")

        submit = st.form_submit_button("Calculate Loan")

    if submit and loan_amount and interest_rate and loan_term:
        try:
            response = requests.post(
                "http://backend:8000/api/v1/calculate_loan",
                json={
                    "loan_amount": loan_amount,
                    "interest_rate": interest_rate,
                    "loan_term_months": loan_term
                }
            )
            if response.ok:
                result = response.json()
                st.success(f"Congratulations {full_name}, your loan calculation is complete!")
                st.info("Calculation Results")
                cols = st.columns(3)
                with cols[0]: st.metric("Monthly Payment", f"${result['monthly_payment']:,.2f}")
                with cols[1]: st.metric("Total Interest", f"${result['total_interest']:,.2f}")
                with cols[2]: st.metric("Total Payment", f"${result['total_payment']:,.2f}")
                
                # Get payment schedule
                schedule_response = requests.post(
                    "http://backend:8000/api/v1/generate_payment_schedule",
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
                    st.markdown("Download the payment schedule as CSV and submit it in your loan application.")
                    st.download_button(
                        label="Download Payment Schedule",
                        data=csv,
                        file_name='payment_schedule.csv',
                        mime='text/csv'
                    )
        except Exception as e:
            st.error(f"Error calculating loan: {str(e)}")

# Loan Application Form
with tab3:
    st.header("Loan Application Form")
    st.write("Please fill out the loan application form to proceed with your loan request.")
    
   