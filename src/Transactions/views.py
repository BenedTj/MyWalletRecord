from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from .models import Transaction
from .forms import TransactionForm1, TransactionForm2_Expense, TransactionForm2_Income, LoginForm, RegisterForm
from .calculations import MoneyCalculations
from decimal import Decimal

class user_homepage(View):
    def get(self, request):
        FormInstance = TransactionForm1()
        MoneyCalculator = MoneyCalculations(Transaction.objects.all())
        context = {
            'form': FormInstance,
            'object_list': Transaction.objects.all(),
            'total_expenditure_of_day': MoneyCalculator.calculate_expenditure_of_day(),
            'total_expenditure_of_month': MoneyCalculator.calculate_expenditure_of_month(),
            'total_expenditure_of_year': MoneyCalculator.calculate_expenditure_of_year(),
        }
        return render(request, 'user_homepage.html', context)
    

    def post(self, request):
        FormInstance = TransactionForm1(request.POST)
        MoneyCalculator = MoneyCalculations(Transaction.objects.all())
        context = {
            'form': FormInstance,
            'object_list': Transaction.objects.all(),
            'total_expenditure_of_day': MoneyCalculator.calculate_expenditure_of_day(),
            'total_expenditure_of_month': MoneyCalculator.calculate_expenditure_of_month(),
            'total_expenditure_of_year': MoneyCalculator.calculate_expenditure_of_year()
        }
        if FormInstance.is_valid():
            # go to the 'second_form' view
            request.session['transaction_type'] = FormInstance.cleaned_data['transaction_type']
            request.session['currency'] = FormInstance.cleaned_data['currency']
            request.session['amount'] = str(Decimal(FormInstance.cleaned_data['amount']))
            return HttpResponseRedirect(reverse_lazy('second_form'))
            
        return render(request, 'user_homepage.html', context)
    
class second_form(View):
    """
    The form generated should differ depending on the type of transaction inputted in first form.
    """
    def get(self, request):
        print(request.session['transaction_type'])
        if request.session['transaction_type'] == 'Expense':
            FormInstance = TransactionForm2_Expense()
        else:
            FormInstance = TransactionForm2_Income()
        context = {
            'form': FormInstance
        }
        return render(request, 'second_form.html', context)
    

    def post(self, request):
        if request.session['transaction_type'] == 'Expense':
            FormInstance = TransactionForm2_Expense(request.POST)
        else:
            FormInstance = TransactionForm2_Income(request.POST)
        if FormInstance.is_valid():
            result_args = {
                'transaction_type': request.session.pop('transaction_type'),
                'currency': request.session.pop('currency'),
                'amount': Decimal(request.session.pop('amount')),
                **FormInstance.cleaned_data
            }
            Transaction.objects.create(**result_args)
            return HttpResponseRedirect(reverse_lazy('user_homepage'))
        
        context = {
            'form': FormInstance
        }
        return render(request, 'second_form.html', context)
    
class login_page(View):
    def get(self, request):
        FormInstance = LoginForm()
        context = {
            'form': FormInstance
        }
        return render(request, 'login_page.html', context)
    
    def post(self, request):
        FormInstance = LoginForm(request.POST)
        context = {
            'form': FormInstance
        }
        return render(request, 'login_page.html', context)
    
class register_page(View):
    def get(self, request):
        FormInstance = RegisterForm()
        context = {
            'form': FormInstance
        }
        return render(request, 'register_page.html', context)
    
    def post(self, request):
        FormInstance = RegisterForm(request.POST)
        context = {
            'form': FormInstance
        }
        return render(request, 'register_page.html', context)