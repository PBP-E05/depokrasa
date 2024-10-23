from django.db import models

# Model for Discount
class Discount(models.Model):
    shop_name = models.CharField(max_length=100)  # Placeholder for shop name until Shop model is available
    discount_percentage = models.FloatField()  # Discount percentage, e.g., 10% or 20%
    start_date = models.DateField()  # Start date of the discount
    end_date = models.DateField()  # End date of the discount

    def __str__(self):
        return f"{self.discount_percentage}% discount at {self.shop_name}"


# Model for Promotion
class Promotion(models.Model):
    promotion_type = models.CharField(max_length=50)  # Type of promotion, e.g., "Buy One Get One" or "Flash Sale"
    description = models.TextField()  # Description of the promotion
    shop_name = models.CharField(max_length=100, null=True, blank=True)  # Placeholder for shop name until Shop model is available
    food_name = models.CharField(max_length=100, null=True, blank=True)  # Placeholder for food name until Food model is available
    start_date = models.DateField()  # Start date of the promotion
    end_date = models.DateField()  # End date of the promotion

    def __str__(self):
        if self.shop_name:
            return f"{self.promotion_type} promotion at {self.shop_name}"
        elif self.food_name:
            return f"{self.promotion_type} promotion for {self.food_name}"
        return "Invalid promotion"
