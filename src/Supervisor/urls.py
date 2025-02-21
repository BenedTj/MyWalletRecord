from django.urls import path

from .views import supervisor_homepage, supervisor_logout

app_name = 'supervisor'

urlpatterns = [
    path('', supervisor_homepage.as_view(), name='panel'),
    path('remove/', supervisor_logout.as_view(), name='logout')
]
