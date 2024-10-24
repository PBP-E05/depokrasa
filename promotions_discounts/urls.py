from django.urls import path
from . import views

app_name = 'promotions_discounts'

urlpatterns = [
    path('list/', views.promotions_and_discounts_list, name='promotions_and_discounts_list'),
    path('import/', views.import_data_from_json, name='import_data'),  # URL untuk mengimpor data dari JSON
    path('', views.show_main, name='show_main'),  # URL untuk halaman utama
]
