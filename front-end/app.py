import streamlit as st
import requests
import pandas as pd

# Main app url to show on the top page 
st.set_page_config(
    page_title="Salary Loan Calculator",
    page_icon="💰",
    layout="wide",
)


# Center the logo and title using columns
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=100)
    st.title("Advance Salary Loan Calculator")

st.divider()

#customer details
st.subheader("This is a simple calculator to help you calculate your advance salary loan and loan amount")
st.markdown("<span style='font-size:1.3em; color:#333;'>Please enter your details below to get started</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
 full_name = st.text_input("FULL NAME", placeholder="Enter your full name")
 employment_status = st.selectbox("EMPLOYMENT STATUS", options=["Employed", "Self-Employed", "Unemployed"])
 employee_id = st.text_input("EMPLOYEE ID", placeholder="Enter your employee ID")

with col2:
 company_name = st.text_input("COMPANY NAME", placeholder="Enter your company name")
 email = st.text_input("EMAIL", placeholder="Enter your email address")
 phone_number = st.text_input("PHONE NUMBER", placeholder="Enter your phone number")

st.subheader("Please select the type of calculator you want to use")

# Creating tabs for different calculators to ease navigation
tab1, tab2 = st.tabs(["Salary Advance Calculator", "Loan Calculator"])

# Salary Advance Calculator Tab
with tab1:
    st.header("Salary Advance Calculator")

    with st.form("advance_calculator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gross_salary = st.number_input("GROSS SALARY", min_value=0.0, step=1000.0)
            st.markdown('<span style="color:#888888;">Gross salary is the total salary before any deductions.</span>', unsafe_allow_html=True)
            pay_frequency = st.selectbox("PAY FREQUENCY", options=["monthly", "biweekly", "weekly"])
            st.markdown('<span style="color:#888888;">Pay frequency is how often you receive your salary.</span>', unsafe_allow_html=True)
        with col2:
            requested_amount = st.number_input("REQUESTED ADVANCE AMOUNT", min_value=0.0, step=100.0)
            st.markdown('<span style="color:#888888;">Requested advance amount is the amount you want to borrow.</span>', unsafe_allow_html=True)

        submit = st.form_submit_button("Calculate Advance")

    if submit:
        if gross_salary and requested_amount:
            # First checking eligibility to get maximum advance
            eligibility_data = {
                "gross_salary": gross_salary,
                "pay_frequency": pay_frequency,
                "requested_amount": requested_amount
            }
            result = call_backend("calculate_advance", eligibility_data)
            
            if result:
                # This shows eligibility and maximum advance message
                st.success(f"Congratulations! You are eligible for an advance!")

                # If requested amount is within limits, this shows the calculation results
                if requested_amount <= result['max_advance']:
                    st.info("Below are the details of your advance calculation:")
                    
                    # Display results in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Maximum Advance", f"${result['max_advance']:,.2f}")
                    
                    with col2:
                        st.metric("Approved Amount", f"${result['approved_amount']:,.2f}")
                    
                    with col3:
                        st.metric("Fee", f"${result['fee']:,.2f}")
                    
                    st.metric("Total Repayable", f"${result['total_repayable']:,.2f}")
                else:
                    st.warning(f"⚠️ Your requested amount (${requested_amount:,.2f}) exceeds the maximum advance available (${result['max_advance']:,.2f}). Please adjust your request.")
        else:
            st.error("Please fill in all required fields.")



# Loan Calculator Tab
with tab2:
    st.header("Loan Calculator")
    
    with st.form("loan_calculator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
            st.markdown('<span style="color:#888888;">Loan amount is the total amount you want to borrow.</span>', unsafe_allow_html=True)
            interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
            st.markdown('<span style="color:#888888;">Interest rate is the yearly percentage rate for the loan.</span>', unsafe_allow_html=True)

        with col2:
            loan_term = st.number_input("Loan Term (months)", min_value=1, max_value=360, step=1)
            st.markdown('<span style="color:#888888;">Loan term is the duration for which you want to borrow the money.</span>', unsafe_allow_html=True)

        submit = st.form_submit_button("Calculate Loan")

    if submit:
        if loan_amount and interest_rate and loan_term:
            data = {
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term_months": loan_term
            }
            result = call_backend("calculate_loan", data)
        else:
            st.error("Please fill in all required fields.")

            if submit:
                st.success("Loan Calculation Complete!")
                st.success(f"Below are the results based on your inputs:")
                
                # Display summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Monthly Payment", f"${result['monthly_payment']:,.2f}")
                
                with col2:
                    st.metric("Total Interest", f"${result['total_interest']:,.2f}")
                
                with col3:
                    st.metric("Total Payment", f"${result['total_payment']:,.2f}")
                
                # Display payment schedule
                st.subheader("Below is your payment schedule for the loan:")
                display_payment_schedule(result['payment_schedule']) 

                # Download payment schedule as CSV
                csv = convert_to_csv(result['payment_schedule'])
                st.download_button(
                    label="Download Payment Schedule",
                    data=csv,
                    file_name='payment_schedule.csv',
                    mime='text/csv'
                )