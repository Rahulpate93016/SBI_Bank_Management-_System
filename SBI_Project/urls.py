from django.contrib import admin
from django.urls import path
from testapp import views

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    path('home/', views.home_views, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Customer URLs
    path('customer/', views.customer_login, name='customer_login'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-profile/', views.customer_profile, name='customer_profile'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),
    path('check-balance/', views.check_balance, name='check_balance'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('loan-application/', views.loan_application, name='loan_application'),
    path('my-loan-applications/', views.my_loan_applications, name='my_loan_applications'),

    # Employee URLs
    path('employee-login/', views.employee_login, name='employee_login'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee-logout/', views.employee_logout, name='employee_logout'),

    # Banking Operations
    path('open-new-account/', views.open_new_account, name='open_new_account'),
    path('deposit-money/', views.deposit_money, name='deposit_money'),
    path('withdraw-money/', views.withdraw_money, name='withdraw_money'),

    # Customer Management
    path('view-all-customers/', views.view_all_customers, name='view_all_customers'),

    # Employee Transaction History
    path('employee-transaction-history/', views.employee_transaction_history, name='employee_transaction_history'),

    # Loan Management
    path('manage-loan-applications/', views.manage_loan_applications, name='manage_loan_applications'),
]
