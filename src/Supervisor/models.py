from django.db import models
from django.utils import timezone

class SupervisorRecord(models.Model):
    supervisor = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    superviseeid = models.IntegerField(blank=False, null=False)

class PendingConnections(models.Model):
    supervisor = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    superviseeid = models.IntegerField(blank=False, null=False)
    dateandtime = models.DateTimeField(default=timezone.datetime.now(), blank=False, null=False)

class ActivityHistory(models.Model):
    supervisor = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    superviseeid = models.IntegerField(blank=False, null=False)
    dateandtime = models.DateTimeField(default=timezone.datetime.now(), blank=False, null=False)
    activitytype = models.CharField(max_length=100, default='Connection Request', choices=[('Supervisor Login', 'Supervisor Login'), ('Supervisor End', 'Supervisor End'), ('Supervisee End', 'Supervisee End'), ('Connection Request', 'Connection Request')])

    class Meta:
        ordering = ("-dateandtime",)

class ConnectionRequestHistory(ActivityHistory):
    pending = models.BooleanField(default=True, blank=False, null=False)
    approved = models.BooleanField(default=False, blank=False, null=False)

class CurrentActivity(models.Model):
    supervisorrecord = models.ForeignKey(SupervisorRecord, on_delete=models.CASCADE, blank=False, null=False)
    activityhistory = models.ForeignKey(ActivityHistory, on_delete=models.CASCADE, blank=False, null=False)