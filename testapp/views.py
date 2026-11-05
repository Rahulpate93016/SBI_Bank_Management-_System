
from .models import (
    Customer,
    BankAccount,
    Transaction,
    BankEmployee,
    LoanApplication
)

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction

from decimal import Decimal, InvalidOperation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import secrets
from django.utils.dateparse import parse_date


# ==========================================
# HOME PAGE
# ==========================================

def home_views(request):
    return render(request, 'testapp/Home.html')


# ==========================================
# ADMIN LOGIN
# ==========================================

def admin_login(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            login(request, user)
            return redirect('admin:index')

        messages.error(request, 'Invalid Admin Username or Password')

    return render(request, 'testapp/admin_login.html')


# ==========================================
# ADMIN LOGOUT
# ==========================================

@login_required
def admin_logout(request):

    if not request.user.is_superuser:
        return redirect('home')

    logout(request)
    return redirect('admin_login')


# ==========================================
# CUSTOMER LOGIN
# ==========================================

def customer_login(request):

    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            return redirect('customer_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and not user.is_superuser:

            if Customer.objects.filter(user=user).exists():

                if BankEmployee.objects.filter(user=user).exists():
                    messages.error(request, 'Please use Employee Login.')
                    return redirect('employee_login')

                login(request, user)
                return redirect('customer_dashboard')

            messages.error(request, 'Customer Account Not Found')

        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'testapp/customer_login.html')


# ==========================================
# CUSTOMER DASHBOARD
# ==========================================

@login_required(login_url='customer_login')
def customer_dashboard(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    accounts = BankAccount.objects.filter(customer=customer)

    return render(
        request,
        'testapp/customer_dashboard.html',
        {
            'customer': customer,
            'accounts': accounts
        }
    )


# ==========================================
# CUSTOMER PROFILE
# ==========================================

@login_required(login_url='customer_login')
def customer_profile(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    accounts = BankAccount.objects.filter(customer=customer)

    return render(
        request,
        'testapp/customer_profile.html',
        {
            'customer': customer,
            'accounts': accounts
        }
    )


# ==========================================
# CUSTOMER LOGOUT
# ==========================================

@login_required(login_url='customer_login')
def customer_logout(request):

    if not Customer.objects.filter(user=request.user).exists():
        return redirect('customer_login')

    logout(request)
    return redirect('customer_login')


# ==========================================
# CHECK BALANCE
# ==========================================

@login_required(login_url='customer_login')
def check_balance(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    accounts = BankAccount.objects.filter(customer=customer)

    return render(
        request,
        'testapp/check_balance.html',
        {'accounts': accounts}
    )


# ==========================================
# TRANSACTION HISTORY
# ==========================================

@login_required(login_url='customer_login')
def transaction_history(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    transactions = Transaction.objects.filter(
        account__customer=customer
    ).select_related('account').order_by('-transaction_date')

    return render(
        request,
        'testapp/transaction_history.html',
        {'transactions': transactions}
    )


# ==========================================
# LOAN APPLICATION
# ==========================================

@login_required(login_url='customer_login')
def loan_application(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    if request.method == 'POST':

        loan_type = request.POST.get('loan_type', '')
        loan_amount_input = request.POST.get('loan_amount', '')
        monthly_income_input = request.POST.get('monthly_income', '')
        employment_type = request.POST.get('employment_type', '').strip()
        purpose = request.POST.get('purpose', '').strip()

        try:

            loan_amount = Decimal(loan_amount_input)
            monthly_income = Decimal(monthly_income_input)

            valid_loan_types = [
                'Personal', 'Home', 'Education', 'Business', 'Car'
            ]

            if loan_type not in valid_loan_types:
                raise ValueError('Invalid loan type.')

            if not loan_amount.is_finite() or loan_amount <= 0:
                raise ValueError('Enter a valid loan amount.')

            if not monthly_income.is_finite() or monthly_income <= 0:
                raise ValueError('Enter a valid monthly income.')

            if not employment_type or not purpose:
                raise ValueError('Please fill all required fields.')

            LoanApplication.objects.create(
                customer=customer,
                loan_type=loan_type,
                loan_amount=loan_amount,
                monthly_income=monthly_income,
                employment_type=employment_type,
                purpose=purpose
            )

            messages.success(
                request,
                'Loan Application Submitted Successfully!'
            )

            return redirect('loan_application')

        except (InvalidOperation, ValueError) as error:
            messages.error(request, str(error))

    return render(request, 'testapp/loan_application.html')


# ==========================================
# MY LOAN APPLICATIONS
# ==========================================

@login_required(login_url='customer_login')
def my_loan_applications(request):

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        messages.error(request, 'Customer profile not found.')
        return redirect('customer_login')

    applications = LoanApplication.objects.filter(
        customer=customer
    ).order_by('-application_date')

    return render(
        request,
        'testapp/my_loan_applications.html',
        {'applications': applications}
    )


# ==========================================
# EMPLOYEE LOGIN
# ==========================================

def employee_login(request):

    if request.user.is_authenticated:
        if BankEmployee.objects.filter(user=request.user).exists():
            return redirect('employee_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and not user.is_superuser:

            if BankEmployee.objects.filter(user=user).exists():

                if Customer.objects.filter(user=user).exists():
                    messages.error(request, 'Please use Customer Login.')
                    return redirect('customer_login')

                login(request, user)
                return redirect('employee_dashboard')

            messages.error(request, 'Employee account not found.')

        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'testapp/employee_login.html')


# ==========================================
# EMPLOYEE DASHBOARD
# ==========================================

@login_required(login_url='employee_login')
def employee_dashboard(request):

    employee = BankEmployee.objects.filter(user=request.user).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    return render(
        request,
        'testapp/employee_dashboard.html',
        {'employee': employee}
    )


# ==========================================


# ==========================================
# OPEN NEW BANK ACCOUNT
# ==========================================

@login_required(login_url='employee_login')
@permission_required(('testapp.add_customer', 'testapp.add_bankaccount', 'testapp.add_transaction'), raise_exception=True)
def open_new_account(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    if request.method == 'POST':

        # Customer Details
        name = request.POST.get('name', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        email = request.POST.get('email', '').strip()
        pan_number = request.POST.get('pan_number', '').strip().upper()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        gender = request.POST.get('gender', '').strip()
        address = request.POST.get('address', '').strip()

        # Bank Account Details
        account_type = request.POST.get('account_type', '')
        branch_name = request.POST.get('branch_name', '').strip()
        opening_balance = request.POST.get('opening_balance', '').strip()

        # Nominee Details
        nominee_name = request.POST.get('nominee_name', '').strip()
        nominee_relation = request.POST.get('nominee_relation', '').strip()

        try:

            # Required Field Validation
            if not all([
                name, mobile, email, date_of_birth,
                gender, address, account_type,
                branch_name, opening_balance,
                nominee_name, nominee_relation
            ]):
                raise ValueError('Please fill all required fields.')

            # Mobile Validation
            if not mobile.isdigit() or not (10 <= len(mobile) <= 15):
                raise ValueError('Enter a valid mobile number.')

            # Email Validation
            try:
                validate_email(email)
            except ValidationError:
                raise ValueError('Enter a valid email address.')

            # PAN Validation
            if pan_number and (
                len(pan_number) != 10 or
                not pan_number[:5].isalpha() or
                not pan_number[5:9].isdigit() or
                not pan_number[9].isalpha()
            ):
                raise ValueError('Enter a valid PAN number.')

            # Date of Birth Validation
            dob = parse_date(date_of_birth)

            if dob is None:
                raise ValueError('Enter a valid date of birth.')

            # Gender Validation
            if gender not in ['Male', 'Female', 'Other']:
                raise ValueError('Select a valid gender.')

            # Account Type Validation
            if account_type not in ['Saving', 'Current']:
                raise ValueError('Select a valid account type.')

            # Opening Balance Validation
            balance = Decimal(opening_balance)

            if not balance.is_finite() or balance < 0:
                raise ValueError('Opening balance cannot be negative.')

            # Existing Mobile Check
            if User.objects.filter(username=mobile).exists():
                raise ValueError('This mobile number already has a login.')

            # Transaction Start
            with transaction.atomic():

                # Generate Customer Password
                password = secrets.token_urlsafe(10)

                # Create Customer User
                user = User.objects.create_user(
                    username=mobile,
                    password=password,
                    first_name=name,
                    email=email
                )

                # Create Customer Profile
                customer = Customer.objects.create(
                    user=user,
                    name=name,
                    mobile=mobile,
                    email=email,
                    pan_number=pan_number or None,
                    date_of_birth=dob,
                    gender=gender,
                    address=address
                )

                # Create Bank Account
                account = BankAccount.objects.create(
                    customer=customer,
                    account_type=account_type,
                    balance=balance,
                    branch_name=branch_name,
                    nominee_name=nominee_name,
                    nominee_relation=nominee_relation
                )

                # Initial Deposit Transaction
                if balance > 0:

                    Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=balance,
                        description='Initial Account Opening Deposit'
                    )

            messages.success(
                request,
                'Customer and bank account created successfully!'
            )

            return render(
                request,
                'testapp/open_new_account.html',
                {
                    'success': True,
                    'customer': customer,
                    'account': account,
                    'username': mobile,
                    'password': password
                }
            )

        except (ValueError, InvalidOperation) as error:

            messages.error(request, str(error))

    return render(
        request,
        'testapp/open_new_account.html'
    )


# ==========================================
# DEPOSIT MONEY
# ==========================================

@login_required(login_url='employee_login')
@permission_required(('testapp.change_bankaccount', 'testapp.add_transaction'), raise_exception=True)
def deposit_money(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    if request.method == 'POST':

        account_number = request.POST.get(
            'account_number', ''
        ).strip()

        amount_input = request.POST.get(
            'amount', ''
        ).strip()

        try:

            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise ValueError('Enter a valid positive amount.')

            with transaction.atomic():

                account = BankAccount.objects.select_for_update().get(
                    account_number=account_number
                )

                if account.account_status != 'Active':
                    raise ValueError('This bank account is not active.')

                account.balance += amount

                account.save(update_fields=['balance'])

                Transaction.objects.create(
                    account=account,
                    transaction_type='Deposit',
                    amount=amount,
                    description=f'Deposit processed by {employee.name}'
                )

            messages.success(
                request,
                f'₹{amount} deposited successfully!'
            )

            return redirect('deposit_money')

        except BankAccount.DoesNotExist:
            messages.error(request, 'Account number not found.')

        except (InvalidOperation, ValueError) as error:
            messages.error(request, str(error))

    return render(
        request,
        'testapp/deposit_money.html',
        {'employee': employee}
    )




@login_required(login_url='employee_login')
@permission_required(('testapp.change_bankaccount', 'testapp.add_transaction'), raise_exception=True)
def withdraw_money(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    if request.method == 'POST':

        account_number = request.POST.get(
            'account_number', ''
        ).strip()

        amount_input = request.POST.get(
            'amount', ''
        ).strip()

        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise ValueError('Enter a valid positive amount.')

            with transaction.atomic():

                account = BankAccount.objects.select_for_update().get(
                    account_number=account_number
                )

                if account.account_status != 'Active':
                    raise ValueError('Account is not active.')

                if account.balance < amount:
                    raise ValueError('Insufficient account balance.')

                account.balance -= amount
                account.save(update_fields=['balance'])

                Transaction.objects.create(
                    account=account,
                    transaction_type='Withdrawal',
                    amount=amount,
                    description=f'Withdrawal processed by {employee.name}'
                )

            messages.success(
                request,
                f'₹{amount} withdrawn successfully!'
            )

            return redirect('withdraw_money')

        except BankAccount.DoesNotExist:
            messages.error(request, 'Account number not found.')

        except (InvalidOperation, ValueError) as error:
            messages.error(request, str(error))

    return render(
        request,
        'testapp/withdraw_money.html',
        {'employee': employee}
    )

# ==========================================
# SEARCH CUSTOMER BY ACCOUNT NUMBER
# ==========================================

@login_required(login_url='employee_login')
@permission_required('testapp.view_customer', raise_exception=True)
def view_all_customers(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    customer = None
    accounts = None
    searched = False

    if request.method == 'POST':

        account_number = request.POST.get(
            'account_number', ''
        ).strip()

        searched = True

        if not account_number:
            messages.error(request, 'Enter account number.')

        else:
            account = BankAccount.objects.select_related(
                'customer'
            ).filter(
                account_number=account_number
            ).first()

            if account:
                customer = account.customer

                # Customer ke sabhi bank accounts
                accounts = BankAccount.objects.filter(
                    customer=customer
                )

            else:
                messages.error(
                    request,
                    'No customer found with this account number.'
                )

    return render(
        request,
        'testapp/view_all_customers.html',
        {
            'customer': customer,
            'accounts': accounts,
            'searched': searched
        }
    )

# ==========================================
# EMPLOYEE TRANSACTION HISTORY
# ==========================================

@login_required(login_url='employee_login')
@permission_required('testapp.view_transaction', raise_exception=True)
def employee_transaction_history(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    account = None
    transactions = None

    if request.method == 'POST':

        account_number = request.POST.get(
            'account_number', ''
        ).strip()

        if not account_number:
            messages.error(request, 'Enter account number.')

        else:
            account = BankAccount.objects.select_related(
                'customer'
            ).filter(
                account_number=account_number
            ).first()

            if account:
                transactions = Transaction.objects.filter(
                    account=account
                ).order_by('-transaction_date')

            else:
                messages.error(
                    request,
                    'Account number not found.'
                )

    return render(
        request,
        'testapp/employee_transaction_history.html',
        {
            'account': account,
            'transactions': transactions
        }
    )


# ==========================================
# LOAN APPLICATION MANAGEMENT
# ==========================================

@login_required(login_url='employee_login')
@permission_required(('testapp.view_loanapplication', 'testapp.change_loanapplication'), raise_exception=True)
def manage_loan_applications(request):

    employee = BankEmployee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        messages.error(request, 'Employee access required.')
        return redirect('employee_login')

    if request.method == 'POST':

        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        application = LoanApplication.objects.filter(
            id=application_id
        ).first()

        if application is None:
            messages.error(request, 'Loan application not found.')

        elif application.status != 'Pending':
            messages.warning(
                request,
                'This application has already been processed.'
            )

        elif action == 'approve':
            application.status = 'Approved'
            application.save()

            messages.success(
                request,
                'Loan application approved successfully.'
            )

        elif action == 'reject':
            application.status = 'Rejected'
            application.save()

            messages.success(
                request,
                'Loan application rejected successfully.'
            )

        else:
            messages.error(request, 'Invalid action.')

        return redirect('manage_loan_applications')

    applications = LoanApplication.objects.select_related(
        'customer'
    ).all().order_by('-application_date')

    return render(
        request,
        'testapp/manage_loan_applications.html',
        {'applications': applications}
    )


@login_required(login_url='employee_login')
def employee_logout(request):
    logout(request)
    return redirect('employee_login')
