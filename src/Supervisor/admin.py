from django.contrib import admin
from .models import SupervisorRecord, PendingConnections, ActivityHistory, ConnectionRequestHistory, CurrentActivity

admin.site.register(SupervisorRecord)
admin.site.register(PendingConnections)
admin.site.register(ActivityHistory)
admin.site.register(ConnectionRequestHistory)
admin.site.register(CurrentActivity)