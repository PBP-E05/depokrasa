from django.urls import path
from . import views

app_name = 'promotions_discounts'

urlpatterns = [
    path('list/', views.promotions_and_discounts_list, name='promotions_and_discounts_list'),
    path('import/', views.import_data_from_json, name='import_data'),  # URL for importing data from JSON
    path('delete_expired/', views.delete_expired_discounts, name='delete_expired_discounts'),  # URL for AJAX request to delete expired discounts
    path('main/', views.show_main, name='show_main'),  # Updated URL for main page
]
