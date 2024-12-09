from django.urls import path
from authentication.views import login, register, logout, login_user, logout_user, register_user

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('login-user/', login_user, name='login_user'),
    path('logout-user/', logout_user, name='logout_user'),
    path('register-user/', register_user, name='register_user'),
]