from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

from Transactions.views import LoginMixin
from Transactions.models import Transaction
from .models import SupervisorRecord, PendingConnections, ConnectionRequestHistory, ActivityHistory, CurrentActivity
from .forms import SuperviseeForm

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = 'Supervisor'
    def test_func(self):
        return self.request.user.groups.filter(name=self.group_required).exists()

class supervisor_homepage(LoginMixin, GroupRequiredMixin, View):
    def get(self, request):
        has_supervisee = SupervisorRecord.objects.filter(supervisor=request.user).exists()
        if has_supervisee:
            request.session['alert_message'] = "User {} has approved connection request".format(request.user.username)
            request.session['pending'] = False
            request.session['approved'] = True
        # update alert_message
        if 'alert_message' not in request.session:
            alert_message = ""
        else:
            alert_message = request.session['alert_message']

        # update pending
        if 'pending' not in request.session:
            pending = False
        else:
            pending = request.session['pending']

        # update approved
        if 'approved' not in request.session:
            approved = False
        else:
            approved = request.session['approved']
        
        if has_supervisee:
            supervising_record = SupervisorRecord.objects.get(supervisor=request.user)
            id = supervising_record.superviseeid
            user = User.objects.get(id=id)
            records = Transaction.objects.filter(user=user)
            context = {
                'has_supervisee': has_supervisee,
                'alert_message': alert_message,
                'pending': pending,
                'approved': approved,
                'supervisee': user.username,
                'records': records,
                'requests': PendingConnections.objects.count() + CurrentActivity.objects.count()
            }
            activity_history_parameter = {
                'supervisor': user,
                'superviseeid': id,
                'dateandtime': timezone.datetime.now(),
                'activitytype': 'Supervisor Login'
            }
            activity_history = ActivityHistory(**activity_history_parameter)
            activity_history.save()
            CurrentActivity.objects.create(supervisorrecord=supervising_record, activityhistory=activity_history)
        else:
            FormInstance = SuperviseeForm()
            context = {
                'form': FormInstance,
                'alert_message': alert_message,
                'pending': pending,
                'approved': approved,
                'has_supervisee': has_supervisee,
                'requests': PendingConnections.objects.count() + CurrentActivity.objects.count()
            }
        return render(request, 'Supervisor/supervisor_homepage.html', context)
    
    def post(self, request):
        FormInstance = SuperviseeForm(request.POST)

        # update alert_message
        if 'alert_message' not in request.session:
            alert_message = ""
        else:
            alert_message = request.session['alert_message']

        # update pending
        if 'pending' not in request.session:
            pending = False
        else:
            pending = request.session['pending']

        # update approved
        if 'approved' not in request.session:
            approved = False
        else:
            approved = request.session['approved']
        
        id = request.POST['id']
        has_supervisee = SupervisorRecord.objects.filter(supervisor=request.user).exists()

        if has_supervisee:
            return HttpResponseRedirect(reverse_lazy('supervisor:panel'))
        elif not User.objects.filter(id=id).exists():
            alert_message = "User does not exist"
            return HttpResponseRedirect(reverse_lazy('supervisor:panel'))
        else:
            dateandtime = timezone.datetime.now()
            PendingConnections.objects.create(supervisor=request.user, superviseeid=id, dateandtime=dateandtime)
            ConnectionRequestHistory.objects.create(supervisor=request.user, superviseeid=id, dateandtime=dateandtime, pending=True, approved=False)
            request.session['alert_message'] = "Please wait for user {} to approve connection request".format(User.objects.get(id=id).username)
            request.session['pending'] = True
            request.session['approved'] = False
            return HttpResponseRedirect(reverse_lazy('supervisor:panel'))
        context = {
            'form': FormInstance,
            'alert_message': alert_message,
            'pending': pending,
            'approved': approved,
            'has_supervisee': has_supervisee,
            'requests': PendingConnections.objects.count() + CurrentActivity.objects.count()
        }
        return render(request, "Supervisor/supervisor_homepage.html", context)
    
class supervisor_logout(LoginMixin, GroupRequiredMixin, View):
    def get(self, request):
        supervising_record = SupervisorRecord.objects.get(supervisor=request.user)

        context = {
            'supervisee': User.objects.get(id=supervising_record.superviseeid)
        }
        activity_history_parameter = {
            'supervisor': request.user.id,
            'superviseeid': supervising_record.superviseeid,
            'dateandtime': timezone.datetime.now(),
            'activitytype': 'Supervisor End'
        }
        ActivityHistory.objects.create(**activity_history_parameter)
        current_activities = CurrentActivity.objects.get(supervisorrecord=supervising_record)
        current_activities.delete()
        supervising_record.delete()
        return render(request, 'Supervisor/supervisor_logout.html', context)