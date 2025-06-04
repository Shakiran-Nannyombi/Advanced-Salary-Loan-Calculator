import streamlit as st
import requests
import pandas as pd

API_URL = "https://advanced-salary-loan-calculator.onrender.com"

st.header("SALARY ADVANCE LOAN CALCULATOR")

st.write("Welcome to the Salary Advance Loan Calculator!")
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


def mainInputs(
    gross_pay=0.0, loan_amount=0.0, loan_duration=1, variable_interest_rate=0.0
):
    gross_pay = st.number_input(
        "Gross Pay (in Shillings)", min_value=0.0, step=100.0, format="%.2f", help="shs"
    )
    st.session_state.gross_pay = gross_pay
    st.write("Note: Gross pay is the total earnings before any deductions.")

    loan_amount = st.number_input(
        "Loan Amount (in Shillings)",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        help="shs",
    )
    st.session_state.loan_amount = loan_amount

    loan_duration = st.number_input("Loan Duration (Months)", min_value=1, step=1)
    st.session_state.loan_duration = loan_duration

    variable_interest_rate = st.number_input(
        "Interest Rate (%)", min_value=0.0, step=0.1
    )
    st.session_state.variable_interest_rate = variable_interest_rate
    st.write("Note: The interest rate is variable and may change over time.")

    if st.button("Calculate"):
        # Call the backend to get maximum eligible advance amount and eligibility
        advance_response = requests.post(
            f"{API_URL}/calculate-advance",
            json={
                "gross_pay": gross_pay,
                "advance_duration": 1, # Fixed duration for advance
                "variable_interest_rate": variable_interest_rate,
            },
        )

        if advance_response.status_code == 200:
            advance_result = advance_response.json()
            max_advance_amount = advance_result.get('max_advance_amount', 0.0)
            advance_eligible = advance_result.get("eligible", False)

            st.write(f"Maximum Eligible Advance Amount (40% of Gross Pay): {max_advance_amount:.2f} Shillings")
            st.write("Advance Eligibility:", advance_eligible)

            if advance_eligible:
                # If advance eligible, proceed to calculate loan details for the requested loan amount
                loan_response = requests.post(
                    f"{API_URL}/calculate-loan",
                    json={
                        "gross_pay": gross_pay, # Still send gross_pay
                        "loan_amount": loan_amount,
                        "loan_duration": loan_duration,
                        "variable_interest_rate": variable_interest_rate,
                    },
                )

                if loan_response.status_code == 200:
                    loan_result = loan_response.json()
                    st.write("Monthly Payment:", loan_result.get("monthly_payment", 0.0))
                    st.write(
                        "Total Payment with Interest:",
                        loan_result.get("total_payment_with_interest", 0.0),
                    )
                else:
                    st.error("Failed to calculate loan details.")
            else:
                st.warning("You are not eligible for the salary advance loan.")
        else:
            st.error("Failed to check advance eligibility.")



if __name__ == "__main__":
    mainInputs()

st.divider()

# Analysis and CSV export section
st.subheader("Loan Analysis")

# reusing the same mainInputs
gross_pay = st.session_state.get("gross_pay", 0.0)
loan_amount = st.session_state.get("loan_amount", 0.0)
loan_duration = st.session_state.get("loan_duration", 1)
variable_interest_rate = st.session_state.get("variable_interest_rate", 0.0)

if st.button("Generate Analysis & Download CSV"):
    # getting the calculation result
    calc_response = requests.post(
        f"{API_URL}/calculate-loan",
        json={
            "gross_pay": gross_pay,
            "loan_amount": loan_amount,
            "loan_duration": loan_duration,
            "variable_interest_rate": variable_interest_rate,
        },
    )
    if calc_response.status_code == 200:
        calc_result = calc_response.json()
        # sending both input and result to analysis endpoint
        analysis_payload = {
            "gross_pay": gross_pay,
            "loan_amount": loan_amount,
            "loan_duration": loan_duration,
            "variable_interest_rate": variable_interest_rate,
            "eligible": calc_result.get("eligible", False),
            "monthly_payment": calc_result.get("monthly_payment", 0.0),
            "total_payment_with_interest": calc_result.get(
                "total_payment_with_interest", 0.0
            ),
        }
        analysis_response = requests.post(
            f"{API_URL}/loan-analysis", json=analysis_payload
        )
        if analysis_response.status_code == 200:
            data = analysis_response.json()
            # when backend returns a dict, wrap in list for DataFrame
            if isinstance(data, dict):
                data = [data]
            df = pd.DataFrame(data)
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Analysis as CSV file",
                data=csv,
                file_name="loan_analysis.csv",
                mime="text/csv",
            )
        else:
            st.error("Failed to fetch analysis data from backend.")
    else:
        st.error("Failed to calculate loan details.")

st.markdown(
    '<a href="#" style="color:red; text-decoration:underline;" onclick="window.location.reload(); return false;">Reset values</a>',
    unsafe_allow_html=True,
)

# Footer section
st.markdown("---")
st.markdown("Thank you for using the Salary Loan Calculator!")
st.markdown("For any inquiries, please contact us at support@salaryloancalculator.com")
