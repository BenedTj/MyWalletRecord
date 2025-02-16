from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
import re

from .models import Transaction
from .forms import TransactionForm1, TransactionForm2_Expense, TransactionForm2_Income, LoginForm, RegisterForm
from .calculations import MoneyCalculations
from .userchecking import UserChecking

class LoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

class user_homepage(LoginMixin, View):
    def get(self, request):
        FormInstance = TransactionForm1()
        MoneyCalculator = MoneyCalculations(Transaction.objects.all())
        context = {
            'form': FormInstance,
            'object_list': Transaction.objects.filter(user=request.user),
            'is_supervisor': UserChecking.is_member_of_group(request.user.username, 'Supervisor'),
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
            'object_list': Transaction.objects.filter(user=request.user),
            'is_supervisor': UserChecking.is_member_of_group(request.user.username, 'Supervisor'),
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

class second_form(LoginMixin, View):
    """
    The form generated should differ depending on the type of transaction inputted in first form.
    """
    def get(self, request):
        if request.session['transaction_type'] == 'Expense':
            FormInstance = TransactionForm2_Expense()
        else:
            FormInstance = TransactionForm2_Income()
        context = {
            'form': FormInstance,
            'is_supervisor': User.groups.filter(name=request.user.name).exists()
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
                **FormInstance.cleaned_data,
                'user': request.user
            }
            Transaction.objects.create(**result_args)
            return HttpResponseRedirect(reverse_lazy('user_homepage'))
        
        context = {
            'form': FormInstance,
            'is_supervisor': User.groups.filter(name=request.user.name).exists()
        }
        return render(request, 'user_homepage.html', context)
    
class show_user_id(LoginMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'user_id_page.html', context)
   
class login_page(View):
    def get(self, request):
        FormInstance = LoginForm()
        context = {
            'form': FormInstance,
            'alert_message': ""
        }
        return render(request, 'login_page.html', context)
    
    def post(self, request):
        FormInstance = LoginForm(request.POST)
        alert_message = ""
        name = request.POST['name']
        password = request.POST['password']

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        is_email = re.match(email_pattern, name)

        if is_email:
            user = authenticate(email=name, password=password)
        else:
            user = authenticate(username=name, password=password)
        
        if user is not None:
            alert_message = ""
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('user_homepage'))
        elif (not is_email and User.objects.filter(username=name).exists()) or (is_email and User.objects.filter(email=name).exists()):
            alert_message = "Incorrect password"
        else:
            alert_message = "User does not exist"

        context = {
            'form': FormInstance,
            'alert_message': alert_message
        }
        return render(request, 'login_page.html', context)

class register_page(View):
    def get(self, request):
        FormInstance = RegisterForm()
        context = {
            'form': FormInstance,
            'alert_message': ""
        }
        return render(request, 'register_page.html', context)
    
    def post(self, request):
        FormInstance = RegisterForm(request.POST)
        alert_message = ""
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        second_password = request.POST['password_confirm']
        supervisor = request.POST['supervisor']

        if User.objects.filter(username=name).exists() or User.objects.filter(email=email).exists():
            alert_message = "User already exists"
        elif password != second_password:
            alert_message = "Passwords do not match"
        else:
            User.objects.create_user(username=name, email=email, password=password)
            if supervisor:
                supervisor_group = Group.objects.get(name='Supervisor')
                supervisor_group.user_set.add(User.objects.get(username=name))
            else:
                user_group = Group.objects.get(name='Normal User')
                user_group.user_set.add(User.objects.get(username=name))
            alert_message = ""
            return HttpResponseRedirect(reverse_lazy('login'))
        
        context = {
            'form': FormInstance,
            'alert_message': alert_message
        }
        return render(request, 'register_page.html', context)

class logout_page(LoginMixin, View):
    def get(self, request):
        logout(request)
        context = {}
        return render(request, 'logout_page.html', context)