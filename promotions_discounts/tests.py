from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Shop, Food, Discount
from .views import assign_discounts

class DiscountTests(TestCase):
    
    def setUp(self):
        self.shop = Shop.objects.create(name="Test Restaurant")
        self.food1 = Food.objects.create(shop=self.shop, food_name="Test Food 1", price=Decimal('10000.00'))
        self.food2 = Food.objects.create(shop=self.shop, food_name="Test Food 2", price=Decimal('20000.00'))
        
    def test_assign_discounts_to_foods(self):
        restaurants = [{'name': self.shop.name, 'menu': [{'food_name': self.food1.food_name, 'price': str(self.food1.price)},
                                                         {'food_name': self.food2.food_name, 'price': str(self.food2.price)}]}]
        
        discounted_foods = assign_discounts(restaurants)
        
        self.assertEqual(Discount.objects.count(), 1)
        for food in discounted_foods:
            self.assertIn(food['discount_percentage'], [10, 15, 20, 25, 30])
            self.assertTrue(food['discounted_price'] < food['original_price'])
    
    def test_discount_expiry(self):
        expired_discount = Discount.objects.create(
            shop=self.shop,
            discount_percentage=20,
            end_date=timezone.now() - timedelta(days=1)
        )
        
        active_discount = Discount.objects.create(
            shop=self.shop,
            discount_percentage=15,
            end_date=timezone.now() + timedelta(days=2)
        )
        
        Discount.objects.filter(end_date__lt=timezone.now()).delete()
        
        self.assertEqual(Discount.objects.count(), 1)
        self.assertEqual(Discount.objects.first().discount_percentage, 15)

    def test_calculate_discounted_price(self):
        discount_percentage = 25
        end_date = timezone.now() + timedelta(days=3)
        discount = Discount.objects.create(
            shop=self.shop,
            discount_percentage=discount_percentage,
            end_date=end_date
        )
        
        discounted_price = self.food1.price * (Decimal(1) - Decimal(discount_percentage) / Decimal(100))
        
        self.assertEqual(round(discounted_price, 2), round(self.food1.price * Decimal('0.75'), 2))
