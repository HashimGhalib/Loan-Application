from django.contrib import admin
from .models import Borrower, LoanApplication


class BorrowerAdmin(admin.ModelAdmin):
    model = Borrower
    list_display = ('borrower_id', 'profile_picture', 'email', 'first_name', 'last_name',
                    'date_of_birth', 'income', 'phone_number', 'employment_history', 'user',)


class LoanApplicationAdmin(admin.ModelAdmin):
    model = Borrower
    list_display = ('borrower', 'loan_application_id', 'loan_type', 'loan_amount', 'loan_term', 'interest_rate',
                    'application_date', 'status')
#
# class CustomUserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     list_display = ('email', 'first_name', 'last_name', 'is_active')
#     list_filter = ('is_active',)
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)


admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(LoanApplication, LoanApplicationAdmin)

# Register your models here.
