from django.test import TestCase
from .models import Discount, Promotion
from datetime import date

class PromotionsDiscountsTestCase(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            shop_name="Test Shop",
            discount_percentage=15.0,
            start_date=date(2024, 10, 1),
            end_date=date(2024, 12, 31)
        )

        self.promotion = Promotion.objects.create(
            promotion_type="Buy One Get One",
            description="Buy one item and get another one for free",
            shop_name="Promo Shop",
            start_date=date(2024, 10, 1),
            end_date=date(2024, 12, 31)
        )

    def test_discount_creation(self):
        self.assertEqual(self.discount.shop_name, "Test Shop")
        self.assertEqual(self.discount.discount_percentage, 15.0)
        self.assertEqual(self.discount.start_date, date(2024, 10, 1))
        self.assertEqual(self.discount.end_date, date(2024, 12, 31))

    def test_promotion_creation(self):
        self.assertEqual(self.promotion.promotion_type, "Buy One Get One")
        self.assertEqual(self.promotion.description, "Buy one item and get another one for free")
        self.assertEqual(self.promotion.shop_name, "Promo Shop")
        self.assertEqual(self.promotion.start_date, date(2024, 10, 1))
        self.assertEqual(self.promotion.end_date, date(2024, 12, 31))

    def test_discount_validity(self):
        today = date(2024, 10, 23)
        self.assertTrue(self.discount.start_date <= today <= self.discount.end_date)

    def test_promotion_validity(self):
        today = date(2024, 10, 23)
        self.assertTrue(self.promotion.start_date <= today <= self.promotion.end_date)
