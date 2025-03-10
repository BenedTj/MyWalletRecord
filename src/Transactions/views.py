from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
import re

from .models import Transaction
from .forms import TransactionForm1, TransactionForm2_Expense, TransactionForm2_Income, LoginForm, RegisterForm
from .calculations import MoneyCalculations
from .userchecking import UserChecking
from .restrictaccess import RestrictAccessToFrom
from Supervisor.models import SupervisorRecord, PendingConnections, ActivityHistory, ConnectionRequestHistory, CurrentActivity

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
            'requests': PendingConnections.objects.filter(superviseeid=request.user.id).count() + CurrentActivity.objects.filter(activityhistory__superviseeid=request.user.id).count(),
            'is_supervisee': SupervisorRecord.objects.filter(superviseeid=request.user.id).exists()
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
            'total_expenditure_of_year': MoneyCalculator.calculate_expenditure_of_year(),
            'requests': PendingConnections.objects.count() + CurrentActivity.objects.count(),
            'is_supervisee': SupervisorRecord.objects.filter(superviseeid=request.user.id).exists()
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
            'is_supervisor': UserChecking.is_member_of_group(request.user.username, 'Supervisor'),
            'requests': PendingConnections.objects.count() + CurrentActivity.objects.count(),
            'is_supervisee': SupervisorRecord.objects.filter(superviseeid=request.user.id).exists()
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
            'is_supervisor': UserChecking.is_member_of_group(request.user.username, 'Supervisor'),
            'requests': PendingConnections.objects.count() + CurrentActivity.objects.count(),
            'is_supervisee': SupervisorRecord.objects.filter(superviseeid=request.user.id).exists()
        }
        return render(request, 'user_homepage.html', context)
    
class show_user_id(LoginMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'user_id_page.html', context)

class delete_page(LoginMixin, View):
    @RestrictAccessToFrom('user_homepage')
    def get(self, request, id):
        context = {
            'record': Transaction.objects.get(id=id),
            'alert_message': "",
            'id': id
        }
        return render(request, 'delete_page.html', context)
    
    def post(self, request, id):
        object_referred = Transaction.objects.get(id=id)
        if object_referred is not None:
            object_referred.delete()
            return HttpResponseRedirect(reverse_lazy('user_homepage'))
        else:
            alert_message = "Record does not exist"
        context = {
            'record': Transaction.objects.get(id=id),
            'alert_message': alert_message,
            'id': id
        }
        return render(request, 'delete_page.html', context)
    
class notifications_page(LoginMixin, View):
    def get(self, request):
        pending_connection = PendingConnections.objects.filter(superviseeid=request.user.id)
        supervisor_records = SupervisorRecord.objects.filter(superviseeid=request.user.id)
        if supervisor_records.exists():
            supervisor_record = SupervisorRecord.objects.get(superviseeid=request.user.id)
            activities = CurrentActivity.objects.filter(supervisorrecord=supervisor_record)
            context = {
                'already_connected': True,
                'activities': activities
            }
        elif pending_connection.exists():
            context = {
                'connection_requests': pending_connection,
                'already_connected': supervisor_records.exists(),
                'connecting': pending_connection.exists()
            }
        else:
            context = {
                'already_connected': pending_connection,
                'connecting': pending_connection.exists()
            }
        return render(request, 'notifications_page.html', context)

class approve_requests_page(LoginMixin, View):
    @RestrictAccessToFrom('notifications')
    def get(self, request, id):
        pending_connection = PendingConnections.objects.get(id=id)
        context = {
            'connection_request': pending_connection,
            'id': id
        }
        return render(request, 'approve_requests_page.html', context)
    
    def post(self, request, id):
        pending_connection = PendingConnections.objects.get(id=id)
        connection_request_parameters = {
            'supervisor': pending_connection.supervisor,
            'superviseeid': pending_connection.superviseeid,
            'dateandtime': pending_connection.dateandtime,
            'pending': True,
            'approved': False
        }
        connection_request = ConnectionRequestHistory.objects.get(**connection_request_parameters)
        connection_request.pending = False
        if 'RejectRequest' in request.POST:
            connection_request.approved = False
            connection_request.save()
        else:
            connection_request.approved = True
            connection_request.save()
            supervisor_record = SupervisorRecord(supervisor=pending_connection.supervisor, superviseeid=pending_connection.superviseeid)
            supervisor_record.save()
            CurrentActivity.objects.create(supervisorrecord=supervisor_record, activityhistory=connection_request)
        pending_connection.delete()
        return HttpResponseRedirect(reverse_lazy('notifications'))
    
class cancel_supervision(LoginMixin, View):
    def get(self, request):
        supervising_record = SupervisorRecord.objects.get(superviseeid=request.user.id)

        context = {
            'supervisor': supervising_record.supervisor
        }
        activity_history_parameter = {
            'supervisor': supervising_record.supervisor,
            'superviseeid': request.user.id,
            'dateandtime': timezone.datetime.now(),
            'activitytype': 'Supervisee End'
        }
        ActivityHistory.objects.create(**activity_history_parameter)
        current_activities = CurrentActivity.objects.filter(supervisorrecord=supervising_record)
        current_activities.delete()
        supervising_record.delete()
        return render(request, 'cancel_supervision_page.html', context)

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
