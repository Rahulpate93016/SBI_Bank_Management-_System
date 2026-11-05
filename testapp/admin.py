
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Customer,
    BankAccount,
    Transaction,
    LoanApplication,
    BankEmployee
)
import secrets


# =====================================
# CUSTOMER ADMIN
# =====================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('customer_id', 'name', 'mobile', 'email')
    search_fields = ('name', 'mobile')

    @transaction.atomic
    def save_model(self, request, obj, form, change):

        if not change and not obj.user:

            username = obj.mobile
            temporary_password = secrets.token_urlsafe(10)

            user = User.objects.create_user(
                username=username,
                password=temporary_password,
                first_name=obj.name,
                email=obj.email
            )

            obj.user = user

            super().save_model(request, obj, form, change)

            messages.success(
                request,
                f"Customer Login Created! "
                f"User ID: {username} | "
                f"Temporary Password: {temporary_password}"
            )

        else:
            super().save_model(request, obj, form, change)


# =====================================
# BANK ACCOUNT ADMIN
# =====================================

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    list_display = (
        'account_number',
        'customer',
        'account_type',
        'balance',
        'account_status',
        'opening_date'
    )

    search_fields = ('account_number', 'customer__name')
    list_filter = ('account_type', 'account_status')
    readonly_fields = ('account_number', 'opening_date')

    actions = ['reset_customer_password']

    @admin.action(description="Reset selected customer password")
    def reset_customer_password(self, request, queryset):

        for account in queryset:

            user = account.customer.user

            if user is None:
                messages.error(
                    request,
                    f"Login account not found: {account.account_number}"
                )
                continue

            new_password = secrets.token_urlsafe(10)

            user.set_password(new_password)
            user.save()

            messages.success(
                request,
                f"Account: {account.account_number} | "
                f"New Password: {new_password}"
            )


# =====================================
# TRANSACTION ADMIN
# =====================================

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'account',
        'transaction_type',
        'amount',
        'transaction_date'
    )

    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('account__account_number',)
    readonly_fields = ('transaction_date',)


# =====================================
# LOAN APPLICATION ADMIN
# =====================================

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer',
        'loan_type',
        'loan_amount',
        'status',
        'application_date'
    )

    list_filter = ('loan_type', 'status')
    search_fields = ('customer__name',)


# =====================================
# BANK EMPLOYEE ADMIN
# =====================================

@admin.register(BankEmployee)
class BankEmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'name',
        'mobile',
        'email',
        'designation',
        'joining_date'
    )

    search_fields = ('employee_id', 'name', 'mobile')
    list_filter = ('designation',)

    # Automatically create employee login account

    @transaction.atomic
    def save_model(self, request, obj, form, change):

        if not change and not obj.user:

            username = obj.employee_id
            password = secrets.token_urlsafe(10)

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=obj.name,
                email=obj.email
            )

            obj.user = user

            super().save_model(request, obj, form, change)

            messages.success(
                request,
                f"Employee Created Successfully! "
                f"Username: {username} | "
                f"Temporary Password: {password}"
            )

        else:
            super().save_model(request, obj, form, change)
