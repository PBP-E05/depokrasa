from django.contrib import admin
from .models import Restaurant, Menu, Discount, Promotion, UserFavoriteRestaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'restaurant', 'price']
    search_fields = ['food_name', 'restaurant__name']
    list_filter = ['restaurant']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'menu_item', 
        'discount_percentage', 
        'original_price', 
        'discounted_price', 
        'start_time', 
        'duration', 
        'is_active_display'
    ]
    search_fields = ['menu_item__food_name', 'menu_item__restaurant__name']
    list_filter = ['start_time', 'duration']

    def is_active_display(self, obj):
        return obj.is_active()
    is_active_display.boolean = True
    is_active_display.short_description = 'Is Active?'

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['promotion_type', 'restaurant', 'start_date', 'end_date', 'is_active_display']
    search_fields = ['promotion_type', 'restaurant__name']
    list_filter = ['start_date', 'end_date', 'restaurant']

    def is_active_display(self, obj):
        return obj.is_active()
    is_active_display.boolean = True
    is_active_display.short_description = 'Is Active?'
