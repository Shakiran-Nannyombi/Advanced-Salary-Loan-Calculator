# Advanced Salary Loan Calculator

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen?logo=streamlit)](https://advanced-salary-loan-calculator-jyyojcbjax78j433sfeprm.streamlit.app/)
[![FastAPI Backend](https://img.shields.io/badge/Backend-Live%20on%20Render-blue?logo=fastapi)](https://advanced-salary-loan-calculator.onrender.com)

A web application for calculating salary-based loan and advance eligibility, repayments, and exporting loan analysis as CSV. Built with **Streamlit** (frontend) and **FastAPI** (backend).

---

## 🚀 Live Demo

- **Frontend:** [Streamlit App](https://advanced-salary-loan-calculator-jyyojcbjax78j433sfeprm.streamlit.app/)
- **Backend API:** [FastAPI on Render](https://advanced-salary-loan-calculator.onrender.com)

---

## ✨ Features

- **Salary Advance Calculator:**  
  Calculate eligibility and repayment for salary advances.
- **Loan Calculator:**  
  Compute monthly payments, total repayment, and eligibility for salary-based loans.
- **Loan Analysis & CSV Export:**  
  Generate a detailed analysis and download results as a CSV file.
- **Interactive UI:**  
  Simple, user-friendly interface built with Streamlit.

---

## 🗂️ Project Structure

```
feature/
│
├── fastapi-logic/
│   ├── app.py              # FastAPI backend logic
│   ├── Dockerfile
│   └── requirements.txt
│
├── streamlit-ui/
│   ├── app.py              # Streamlit frontend UI
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml      # (Optional) For container orchestration
│
├── LICENSE
├── README.md
└── requirements.txt        # (Optional) Project-wide requirements
```

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Data Handling:** [Pandas](https://pandas.pydata.org/)
- **HTTP Requests:** [Requests](https://docs.python-requests.org/)

---

## 🚀 Getting Started (Local Development)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Shakiran-Nannyombi/Advanced-Salary-Loan-Calculator.git
   cd Advanced-Salary-Loan-Calculator
   ```

2. **Backend Setup:**

   ```bash
   cd feature/fastapi-logic
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

3. **Frontend Setup (in a new terminal):**

   ```bash
   cd feature/streamlit-ui
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. **Open your browser:**  
   Visit [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deploying the Backend on Render

1. **Push your code to GitHub.**
2. **Go to [Render](https://render.com/), create a new Web Service.**
3. **Set the Root Directory to** `feature/fastapi-logic`.
4. **Set the Start Command to:**
   ```
   uvicorn app:app --host 0.0.0.0 --port 10000
   ```
5. **Set the build command (if needed):**
   ```
   pip install -r requirements.txt
   ```
6. **Deploy!**  
   Your backend will be available at a URL like:  
   `https://advanced-salary-loan-calculator.onrender.com`

7. **Update your Streamlit frontend to use this backend URL.**

---

## 📦 Docker Usage

You can use the provided `Dockerfile`s and `docker-compose.yml` for local containerized deployment.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Made with ❤️ by [Your Name]**
