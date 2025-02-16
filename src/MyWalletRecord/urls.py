from django.contrib import admin
from django.urls import path, include
from Transactions.views import (
    user_homepage,
    second_form,
    login_page,
    register_page,
    logout_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page.as_view(), name='login'),
    path('register/', register_page.as_view(), name='register'),
    path('logout/', logout_page.as_view(), name='logout'),
    path('home/', user_homepage.as_view(), name='user_homepage'),
    path('add/', second_form.as_view(), name='second_form'),
    # path('Transactions', include('Transactions.urls'))
]
