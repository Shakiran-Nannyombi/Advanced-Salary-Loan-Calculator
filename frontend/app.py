import streamlit as st
import requests
import pandas as pd

st.header("SALARY LOAN CALCULATOR")

st.write("Welcome to the Salary Loan Calculator!")
st.divider()

# USER inputs
st.subheader("Enter your details below:")
company_name = st.text_input("Company Name")
role = st.text_input("Role")
employee_id = st.text_input("Employee ID")
pay_frequency = st.selectbox("Pay Frequency", ["Monthly", "Bi-Weekly", "Weekly"])
st.write("Note: The pay frequency means how often you receive your salary.")

st.divider()

# Function to calculate loan eligibility and payment details
st.subheader("Loan Eligibility and Payment Details")
def mainInputs(gross_pay=0.0, loan_amount=0.0, loan_duration=1, variable_interest_rate=0.0):
    gross_pay = st.number_input("Gross Pay (in Shillings)", min_value=0.0, step=100.0, format="%.2f", help="shs")
    st.write("Note: Gross pay is the total earnings before any deductions.")
    loan_amount = st.number_input("Loan Amount (in Shillings)", min_value=0.0, step=100.0, format="%.2f", help="shs")
    loan_duration = st.number_input("Loan Duration (Months)", min_value=1, step=1)
    variable_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1)
    st.write("Note: The interest rate is variable and may change over time.")
    
    if st.button("Calculate"):
        response = requests.post("http://localhost:8000/calculate-loan",
            json={
                "gross_pay": gross_pay,
                "loan_amount": loan_amount,
                "loan_duration": loan_duration,
                "variable_interest_rate": variable_interest_rate
            }
        )
        result = response.json()
        st.write("Eligibility:", result.get("eligible", False))
        if result.get("eligible", False):
            st.write("Monthly Payment:", result.get("monthly_payment", 0.0))
            st.write("Total Payment with Interest:", result.get("total_payment_with_interest", 0.0))
        else:
            st.warning("We apologize, you are not eligible for the salary loan.")

    st.markdown(
        '<a href="#" style="color:red; text-decoration:underline;" onclick="window.location.reload(); return false;">Reset values</a>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    mainInputs()
    
st.divider()

# Analysis and CSV export section
st.subheader("Loan Analysis")

if st.button("Generate Analysis & Download CSV"):
    # Request analysis data from backend
    response = requests.get("http://localhost:8000/loan-analysis")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Analysis as CSV file",
            data=csv,
            file_name='loan_analysis.csv',
            mime='text/csv',
        )
    else:
        st.error("Failed to fetch analysis data from backend.")


# Footer section
st.markdown("---")
st.markdown("Thank you for using the Salary Loan Calculator!")
st.markdown("For any inquiries, please contact us at support@salaryloancalculator.com")