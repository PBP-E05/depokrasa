from django.urls import path
from . import views

app_name = 'promotions_discounts'  # Namespace

urlpatterns = [
    path('list/', views.promotions_and_discounts_list, name='promotions_and_discounts_list'),  # Definisikan nama view
]
