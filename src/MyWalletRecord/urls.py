from django.contrib import admin
from django.urls import path, include
from Transactions.views import (
    user_homepage,
    second_form,
    show_user_id,
    delete_page,
    login_page,
    notifications_page,
    approve_requests_page,
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
    path('userid/', show_user_id.as_view(), name='user_id'),
    path('delete/<int:id>', delete_page.as_view(), name='delete'),
    path('requests/', notifications_page.as_view(), name='notifications'),
    path('requests/<int:id>', approve_requests_page.as_view(), name='approve_requests'),
    path('supervisor/', include('Supervisor.urls'))
    # path('Transactions', include('Transactions.urls'))
]
