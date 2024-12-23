from django.contrib import admin
from .models import Discount, Promotion, UserFavoriteRestaurant

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
