from django.contrib import admin
from django.urls import path, include
from Transactions.views import (
    user_homepage,
    second_form
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', user_homepage.as_view(), name='user_homepage'),
    path('add/<str:transaction_type>/<str:currency>/<amount>/', second_form.as_view(), name='second_form'),
    path('Transactions', include('Transactions.urls'))
]
