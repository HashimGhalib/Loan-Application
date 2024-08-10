from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Borrower, LoanApplication


class UserRegForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class BorrowerForm(forms.ModelForm):
    # employment_history = forms.JSONField(widget=forms.Textarea(attrs={'placeholder': 'Enter employment history'}))

    class Meta:
        model = Borrower
        fields = ['profile_picture', 'email', 'first_name', 'last_name', 'date_of_birth', 'income', 'phone_number', 'employment_history']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            # 'profile_picture': forms.FileInput(attrs={'type': 'file'}),

            # PLACE HOLDER
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ghalib'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Hashim'}),
            'income': forms.NumberInput(attrs={'placeholder': '10000.00'}),
            'employment_history': forms.Textarea(attrs={'placeholder': 'Enter employment history'})
        }


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'loan_amount', 'loan_term', 'interest_rate']

        widgets = {
            'interest_rate': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '5%'}),
            # 'loan_type': forms.NumberInput(attrs={'placeholder': 'Personal'}),

            # PLACE HOLDER
            'loan_term': forms.NumberInput(attrs={'placeholder': 'Loan Term (months)'}),
            'loan_amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }






#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name', 'last_name')
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name', 'last_name')
#
#
# class RoleForm(forms.Form):
#     name = forms.CharField(max_length=30)
#     class Meta:
#         model = Role
#         fields = ('name',)
