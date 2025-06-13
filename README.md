# Advanced Salary Loan Calculator

A microservice-based application that provides salary advance and loan calculations with a modern UI.

## 🏗️ Architecture

The application consists of two main components:
- **Frontend**: Streamlit-based user interface
- **Backend**: FastAPI service with Pandas-powered calculations

## 🚀 Features

- Salary advance calculations
- Loan amount and interest calculations
- Compound interest computations
- Interactive UI with real-time results

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Data Processing**: Pandas
- **Containerization**: Docker & Docker Compose
- **Deployment**: VPS

## 📋 Prerequisites

- Docker
- Docker Compose
- Git

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd Advanced-Salary-Loan-Calculator
```

2. Build and run the containers:
```bash
docker compose up --build
```

3. Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

## 📁 Project Structure

```
Advanced-Salary-Loan-Calculator/
├── front-end/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── docker-compose.yml
├── test-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

## 🔧 Development

### Frontend Development
- Located in `front-end/`
- Built with Streamlit
- Handles UI and API calls

### Backend Development
- Located in `backend/`
- Built with FastAPI
- Handles calculations and business logic

### Testing
- Use `test-compose.yml` for running tests in an isolated environment
- Run tests using: `docker compose -f test-compose.yml up`

## 📝 API Documentation

### Endpoints

1. `/calculate_advance`
   - Calculates salary advance eligibility and amount
   - Input: Salary details, requested amount
   - Output: Eligibility status, maximum advance

2. `/calculate_loan`
   - Calculates loan details and interest
   - Input: Loan amount, interest rate, term
   - Output: Total repayable amount, schedule

## 🔐 Security

- API endpoints are protected
- Input validation implemented
- Secure error handling

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
