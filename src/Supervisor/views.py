from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

from Transactions.views import LoginMixin
from Transactions.models import Transaction
from .models import SupervisorRecord
from .forms import SuperviseeForm

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = 'Supervisor'
    def test_func(self):
        return self.request.user.groups.filter(name=self.group_required).exists()

class supervisor_homepage(LoginMixin, GroupRequiredMixin, View):
    def get(self, request):
        has_supervisee = SupervisorRecord.objects.filter(supervisor=request.user).exists()
        if has_supervisee:
            id = SupervisorRecord.objects.get(supervisor=request.user).superviseeid
            user = User.objects.get(id=id)
            records = Transaction.objects.filter(user=user)
            context = {
                'has_supervisee': has_supervisee,
                'alert_message': "",
                'supervisee': user.username,
                'records': records
            }
        else:
            FormInstance = SuperviseeForm()
            context = {
                'form': FormInstance,
                'alert_message': "",
                'has_supervisee': has_supervisee
            }
        return render(request, 'Supervisor/supervisor_homepage.html', context)
    
    def post(self, request):
        FormInstance = SuperviseeForm(request.POST)
        alert_message = ""
        id = request.POST['id']
        has_supervisee = SupervisorRecord.objects.filter(supervisor=request.user).exists()

        if has_supervisee:
            return HttpResponseRedirect(reverse_lazy('supervisor:panel'))
        elif not User.objects.filter(id=id).exists():
            alert_message = "User does not exist"
        else:
            SupervisorRecord.objects.create(supervisor=request.user, superviseeid=id)
            return HttpResponseRedirect(reverse_lazy('supervisor:panel'))
        context = {
            'form': FormInstance,
            'alert_message': alert_message,
            'has_supervisee': has_supervisee
        }
        return render(request, "Supervisor/supervisor_homepage.html", context)
    
class supervisee_logout(LoginMixin, GroupRequiredMixin, View):
    def get(self, request):
        supervising_record = SupervisorRecord.objects.get(supervisor=request.user)
        context = {
            'supervisee': User.objects.get(id=supervising_record.superviseeid)
        }
        supervising_record.delete()
        return render(request, 'Supervisor/supervisor_logout.html', context)