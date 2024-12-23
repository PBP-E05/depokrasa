from django.contrib import admin
from .models import Menu, Restaurant  # Impor model yang ada di aplikasi main

# Register model Menu
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'price', 'restaurant')  # Kolom yang ditampilkan di admin
    search_fields = ('food_name', 'restaurant__name')    # Pencarian berdasarkan nama makanan dan restoran
    list_filter = ('restaurant',)                       # Filter berdasarkan restoran

# Register model Restaurant
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name',)                             # Kolom yang ditampilkan
    search_fields = ('name',)                            # Pencarian berdasarkan nama restoran
