# 🏦 SBI Bank Management System

## 📌 Project Overview

The **SBI Bank Management System** is a web-based banking application developed using Python and Django. The main objective of this project is to manage banking operations digitally through a centralized system.

The application provides separate login access for Admin, Employees, and Customers. It allows customers to manage their bank accounts, perform transactions, check balances, view transaction history, and apply for loans.

Employees can manage customer banking operations, search customer details, process deposits and withdrawals, view transaction records, and manage loan applications. Administrators can manage users, groups, permissions, and application data through the Django Admin Panel.

The project implements role-based access control using Django authentication, Groups, and Permissions.

---

## ✨ Features

### 1. Admin Module
- Secure Admin Login and Logout.
- Django Admin Panel integration.
- Manage Customer records.
- Manage Bank Account records.
- Manage Employee records.
- View and manage Transaction records.
- Manage Loan Applications.
- Create and manage User Groups.
- Assign permissions to different user roles.
- Role-Based Access Control (RBAC).

### 2. Customer Module
- Customer Login and Logout.
- Customer Dashboard.
- View Personal Profile.
- View Bank Account Details.
- Check Available Account Balance.
- View Transaction History.
- Apply for Different Types of Loans.
- View Submitted Loan Applications and their Status.

### 3. Employee Module
- Employee Login and Logout.
- Employee Dashboard.
- Open New Bank Accounts.
- Search Customer Details using Account Number.
- View Customer Profile and Account Information.
- Deposit Money into Customer Accounts.
- Withdraw Money from Customer Accounts.
- View Transaction History.
- View and Manage Loan Applications.
- Approve or Reject Loan Applications.

### 4. Banking Operations

**Account Opening**
- Register new customers and create bank accounts.
- Store account information and nominee details.
- Maintain account types and branch information.

**Deposit**
- Add money to customer bank accounts.
- Record deposit transactions.
- Update account balances.

**Withdrawal**
- Withdraw money from customer bank accounts.
- Maintain withdrawal transaction records.
- Update account balances.

**Balance Enquiry**
- Check the current available account balance.

**Transaction History**
- Maintain records of deposits and withdrawals.
- View transaction types, amounts, dates, and descriptions.

### 5. Loan Management
- Customers can submit loan applications.
- Enter loan type, requested amount, monthly income, employment type, and loan purpose.
- Customers can view their loan application status.
- Employees can review loan applications.
- Employees can approve or reject loan applications.

### 6. Authentication and Authorization
- Separate login access for Admin, Employee, and Customer.
- Django User Authentication.
- Django Groups and Permissions.
- Role-Based Access Control.
- Customer-specific data access.
- Employee-only access to authorized banking operations.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Application Framework |
| SQLite | Database |
| HTML5 | Web Page Structure |
| CSS3 | Web Page Styling |
| Django ORM | Database Operations |
| Django Admin | Administrative Management |
| Git | Version Control |
| GitHub | Source Code Hosting |

---

## 🗄️ Database Models

The project uses Django Models and ORM to manage banking data.

### Customer
Stores customer personal information:
- Customer ID
- User
- Name
- Mobile Number
- Email
- PAN Number
- Date of Birth
- Gender
- Address

### BankAccount
Stores bank account information:
- Account Number
- Customer
- Account Type
- Balance
- Account Status
- Opening Date
- Branch Name
- Nominee Name
- Nominee Relation

### Transaction
Stores banking transaction records:
- Account
- Transaction Type
- Amount
- Transaction Date
- Description

### LoanApplication
Stores loan application details:
- Customer
- Loan Type
- Loan Amount
- Monthly Income
- Employment Type
- Purpose
- Application Status
- Application Date

### BankEmployee
Stores employee information:
- User
- Employee ID
- Name
- Mobile Number
- Email
- Designation
- Joining Date

---

## 📂 Project Structure

```text
SBI_Bank_Management_System/
│
├── SBI_Project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── testapp/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
│
├── Templates/
│   └── testapp/
│       └── HTML Templates
│
├── Static/
│   └── CSS and Static Files
│
├── manage.py
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Rahulpate93016/SBI_Bank_Management-_System.git
```

### Step 2: Open Project Directory

```bash
cd SBI_Bank_Management-_System
```

### Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install Django

```bash
pip install django
```

### Step 6: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## 🔐 User Roles

| Role | Responsibilities |
|---|---|
| Admin | Manage users, records, groups, and permissions |
| Employee | Manage accounts, deposits, withdrawals, customers, and loans |
| Customer | View account details, balance, transactions, and apply for loans |

---

## 🚀 Future Improvements

- Integrate REST APIs using Django REST Framework.
- Add email and SMS notifications.
- Implement OTP-based authentication.
- Add PDF transaction statement generation.
- Integrate online payment functionality.
- Add advanced reporting and analytics.
- Deploy the application to a production server.

---

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Python Programming.
- Django Project and App Structure.
- Django Models and ORM.
- Database Relationships.
- CRUD Operations.
- Django Views and URL Routing.
- HTML Templates and Static Files.
- Django Authentication.
- Django Admin Customization.
- Groups and Permissions.
- Role-Based Access Control.
- Git and GitHub Version Control.

---

## 👨‍💻 Developer

**Rahul Patel**

GitHub: https://github.com/Rahulpate93016

LinkedIn: https://www.linkedin.com/in/rahul-patel-607b29247/

---

## 📜 License

This project is licensed under the MIT License.

---

⭐ If you find this project useful, feel free to explore the repository and provide feedback.
