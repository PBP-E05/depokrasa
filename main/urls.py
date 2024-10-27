from django.urls import path
from main.views import show_main, show_news_json, create_news_ajax, delete_news, add_to_wishlist

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('news-json/', show_news_json, name='show_news_json'),
    path('create-news-ajax/', create_news_ajax, name='create_news_ajax'),
    path('delete-news/<uuid:id>/', delete_news, name='delete_news'),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
]