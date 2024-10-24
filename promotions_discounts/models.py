from django.db import models

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
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='discounts', default=1)  # Set default to an existing shop ID
    discount_percentage = models.FloatField()  # E.g., 10, 15, 20 for 10%, 15%, 20%
    start_date = models.DateField()
    end_date = models.DateField()

    def is_active(self):
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.discount_percentage}% discount at {self.shop.name}"


class Promotion(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='promotions')
    promotion_type = models.CharField(max_length=100)  # E.g., "Buy One Get One"
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def is_active(self):
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.promotion_type} at {self.shop.name}"
