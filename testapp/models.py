
from django.db import models
from django.contrib.auth.models import User
import random


# ==================================================
# FUNCTION: Generate Unique Bank Account Number
# ==================================================

def generate_account_number():

    while True:
        number = str(random.randint(100000000000, 999999999999))

        if not BankAccount.objects.filter(account_number=number).exists():
            return number


# ==================================================
# MODEL 1: CUSTOMER
# ==================================================

class Customer(models.Model):

    customer_id = models.AutoField(primary_key=True)

    # Customer Login Account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Personal Details
    name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    email = models.EmailField()

    pan_number = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    address = models.TextField()

    def __str__(self):
        return self.name


# ==================================================
# MODEL 2: BANK ACCOUNT
# ==================================================

class BankAccount(models.Model):

    account_number = models.CharField(
        max_length=12,
        unique=True,
        default=generate_account_number,
        editable=False
    )

    # Account Owner
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    ACCOUNT_TYPES = [
        ('Saving', 'Saving Account'),
        ('Current', 'Current Account'),
    ]

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    account_status = models.CharField(
        max_length=20,
        default='Active'
    )

    # Branch Details
    branch_name = models.CharField(
        max_length=100,
        blank=True
    )

    # Nominee Details
    nominee_name = models.CharField(
        max_length=100,
        blank=True
    )

    nominee_relation = models.CharField(
        max_length=50,
        blank=True
    )

    opening_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.account_number


# ==================================================
# MODEL 3: TRANSACTION
# ==================================================

class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ]

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_date = models.DateTimeField(auto_now_add=True)

    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.account.account_number} - {self.transaction_type}"


# ==================================================
# MODEL 4: LOAN APPLICATION
# ==================================================

class LoanApplication(models.Model):

    LOAN_TYPES = [
        ('Personal', 'Personal Loan'),
        ('Home', 'Home Loan'),
        ('Education', 'Education Loan'),
        ('Business', 'Business Loan'),
        ('Car', 'Car Loan'),
    ]

    LOAN_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    loan_type = models.CharField(
        max_length=20,
        choices=LOAN_TYPES
    )

    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    employment_type = models.CharField(max_length=50)

    purpose = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        default='Pending'
    )

    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.loan_type}"


# ==================================================
# MODEL 5: BANK EMPLOYEE
# ==================================================

class BankEmployee(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    email = models.EmailField()

    designation = models.CharField(max_length=50)

    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
