from django.db import models
from django.contrib.auth.models import User
from main.models import Menu
import uuid

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
''' To create dummy data, run the following code in the shell:

from django.contrib.auth.models import User
from usermanagement.models import ProductDummy, Wishlist

# Create dummy products
products = [
    {'name': 'Product 1', 'price': 1000, 'description': 'This is product 1'},
    {'name': 'Product 2', 'price': 2000, 'description': 'This is product 2'},
    {'name': 'Product 3', 'price': 3000, 'description': 'This is product 3'},
    {'name': 'Product 4', 'price': 4000, 'description': 'This is product 4'},
    {'name': 'Product 5', 'price': 5000, 'description': 'This is product 5'},
]

for product_data in products:
    ProductDummy.objects.create(**product_data)

# Get a user
user = User.objects.get(username='zero')

# Add products to the user's wishlist
for product in ProductDummy.objects.all():
    Wishlist.objects.create(user=user, product=product)
'''