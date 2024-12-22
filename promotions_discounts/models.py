from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from main.models import Restaurant, Menu
from django.utils.timezone import now
from datetime import timedelta

class Discount(models.Model):
    menu_item = models.ForeignKey('main.Menu', on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.FloatField()  # :3
    original_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Auto-calculated
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Auto-calculated
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField()  
    duration = models.DurationField(editable=False)  

    def is_active(self):
        end_time = self.start_time + self.duration
        return now() <= end_time

    def save(self, *args, **kwargs):
        # Ambil original price dari Menu
        self.original_price = self.menu_item.price
        
        # Hitung discounted price berdasarkan original price dan discount percentage
        discount_factor = Decimal(1) - (Decimal(self.discount_percentage) / Decimal(100))
        self.discounted_price = round(self.original_price * discount_factor, 2)  # Pembulatan 2 desimal

        # Buat waktu heheheheheh
        self.duration = self.end_time - self.start_time
        
        super().save(*args, **kwargs)  # Simpan ke database

    def __str__(self):
        return f"{self.menu_item.food_name} - {self.discount_percentage}% OFF"

class Promotion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='promotions')
    promotion_type = models.CharField(max_length=100, help_text="Tipe promosi, misal 'Beli 1 Gratis 1'")
    description = models.TextField(help_text="Deskripsi detail promosi")
    start_date = models.DateTimeField(help_text="Tanggal dan waktu mulai promosi")
    end_date = models.DateTimeField(help_text="Tanggal dan waktu berakhir promosi")

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.promotion_type} at {self.restaurant.name}"

class UserFavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.user.username}'s favorite restaurant: {self.restaurant.name}"
