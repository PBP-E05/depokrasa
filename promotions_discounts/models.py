from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional, for more details about the shop

    def __str__(self):
        return self.name


class Food(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='foods')
    food_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food_name} ({self.shop.name})"


class Discount(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='discounts')  # Removed default to allow dynamic assignment
    discount_percentage = models.FloatField()  # E.g., 10, 15, 20 for 10%, 15%, 20%
    end_date = models.DateTimeField()  # Changed to DateTimeField to allow more precise timing, like countdowns

    def is_active(self):
        from datetime import datetime
        now = datetime.now()
        return now <= self.end_date

    def __str__(self):
        return f"{self.discount_percentage}% discount at {self.shop.name}"


class Promotion(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='promotions')
    promotion_type = models.CharField(max_length=100)  # E.g., "Buy One Get One"
    description = models.TextField()
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()

    def is_active(self):
        from datetime import datetime
        now = datetime.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.promotion_type} at {self.shop.name}"


class UserFavoriteShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_shops')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='favorited_by')
    weight = models.FloatField(default=1.0) 

    def __str__(self):
        return f"{self.user.username}'s favorite shop: {self.shop.name}"
