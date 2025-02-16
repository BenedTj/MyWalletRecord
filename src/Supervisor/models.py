from django.db import models

class SupervisorRecord(models.Model):
    supervisor = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    superviseeid = models.IntegerField(blank=False, null=False)