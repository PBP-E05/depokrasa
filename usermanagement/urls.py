from django.urls import path
from usermanagement.views import show_wishlist, add_wishlist, delete_wishlist, clear_wishlist, edit_profile

app_name = 'usermanagement'

urlpatterns = [
    path('wishlist/', show_wishlist, name='wishlist'),
    path('wishlist/add/', add_wishlist, name='add_wishlist'),
    path('wishlist/delete/<uuid:id>/', delete_wishlist, name='delete_wishlist'),
    path('wishlist/clear/', clear_wishlist, name='clear_wishlist'),
    path('profile/', edit_profile, name='profile'),
]