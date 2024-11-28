from django.urls import path
from authentication.views import register, login_user, logout_user, login, register_user

app_name = 'authentication'

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login_user, name='login'),
    # path('logout/', logout_user, name='logout'),
    path('login/', login, name='login'),
    path('register/', register_user, name='register'),
]