from django.urls import path
from main.views import show_main, show_news_json, create_news_ajax, delete_news, add_to_wishlist, create_news, edit_news
from . import views

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('news-json/', show_news_json, name='show_news_json'),
    path('create-news/', create_news, name='create_news'),
    path('create-news-ajax/', create_news_ajax, name='create_news_ajax'),
    path('edit-news/<uuid:id>/', edit_news, name='edit_news'),
    path('delete-news/<uuid:id>/', delete_news, name='delete_news'),
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('show-template/', views.my_template_view, name='show_template'),
    path('insert_data/', views.insert_restaurant_data, name='insert_data'),
    path('api/restaurants/', views.get_restaurants, name='get_restaurants'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.get_wishlist, name='get_wishlist'),
    path('wishlist/delete/', views.delete_from_wishlist, name='delete_from_wishlist'),
]