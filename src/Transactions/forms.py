from django import forms
from .models import Transaction

class TransactionForm1(forms.Form):
    transaction_type = forms.ChoiceField(choices=Transaction.TransactionType, required=True)
    currency = forms.ChoiceField(choices=Transaction.CurrencyType, required=True)
    amount = forms.DecimalField(max_digits=15, decimal_places=2, required=True)

class TransactionForm2_Expense(forms.Form):
    date = forms.DateField(required=True, widget=forms.SelectDateWidget)
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=1000, required=False)
    category = forms.ChoiceField(choices=Transaction.ExpenseCategory, required=True)

class TransactionForm2_Income(forms.Form):
    date = forms.DateField(required=True, widget=forms.SelectDateWidget)
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=1000, required=False)
    category = forms.ChoiceField(choices=Transaction.IncomeCategory, required=True)

class LoginForm(forms.Form):
    name = forms.CharField(max_length=1000, required=True)
    password = forms.CharField(max_length=1000, required=True, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=1000, required=True)
    email = forms.CharField(max_length=1000, required=True)
    password = forms.CharField(max_length=1000, required=True, widget=forms.PasswordInput)