from django.db import models
import datetime
import uuid
import random

class FeaturedNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    icon_image = models.ImageField(upload_to='featured_news/icon', blank=True, null=True)
    grand_title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    grand_image = models.ImageField(upload_to='featured_news/grand', blank=True, null=True)

    cooking_time = models.IntegerField()
    calories = models.IntegerField()

    time_added = models.DateField(default=datetime.datetime.now().strftime('%d/%m'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food_name} - {self.restaurant.name}"