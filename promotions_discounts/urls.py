from django.urls import path
from . import views

app_name = 'promotions_discounts'

urlpatterns = [
    path('list/', views.promotions_and_discounts_list, name='promotions_and_discounts_list'),
    path('import/', views.import_data_from_json, name='import_data'),
    path('delete_expired/', views.delete_expired_discounts, name='delete_expired_discounts'),
    path('select_favorites/', views.select_favorite_restaurants, name='select_favorite_restaurants'), 
    path('api/discounts/', views.discounts_list, name='discounts_list'),
    path('api/promotions/', views.promotions_list, name='promotions_list'),
    path('restaurants/', views.get_restaurant_names, name='get_restaurant_names'),
]
