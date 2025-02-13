from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import Transaction
from .forms import TransactionForm1, TransactionForm2_Expense, TransactionForm2_Income
from .calculations import MoneyCalculations

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
            # go to the 'second_form' view (figure out how to send the data to the next view)
            return reverse_lazy('user_services:second_form', kwargs=FormInstance.cleaned_data)
            
        return render(request, 'user_homepage.html', context)
    
class second_form(View):
    """
    The form generated should differ depending on the type of transaction inputted in first form.
    """
    def get(self, request, transaction_type, currency, amount):
        if transaction_type == 'Expense':
            FormInstance = TransactionForm2_Expense()
        else:
            FormInstance = TransactionForm2_Income()
        context = {
            'form': FormInstance
        }
        return render(request, 'second_form.html', context)
    

    def post(self, request, transaction_type, currency, amount):
        if transaction_type == 'Expense':
            FormInstance = TransactionForm2_Expense(request.POST)
        else:
            FormInstance = TransactionForm2_Income(request.POST)
        if FormInstance.is_valid():
            result_args = {
                'transaction_type': transaction_type,
                'currency': currency,
                'amount': amount,
                **FormInstance.cleaned_data
            }
            Transaction.objects.create(**result_args)
            return reverse_lazy('user_services:user_homepage')
        context = {
            'form': FormInstance
        }
        return render(request, 'second_form.html', context)