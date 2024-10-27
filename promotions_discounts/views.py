from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from .models import Shop, Food, Discount, Promotion, UserFavoriteShop
from .forms import FavoriteShopForm
from datetime import timedelta
from django.utils import timezone
import random
from decimal import Decimal
import os
from django.http import HttpResponse, JsonResponse

def load_restaurants():
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

def assign_discounts(restaurants):
    discount_percentages = [10, 15, 20, 25, 30]
    now = timezone.now()
    discounted_foods = []

    for restaurant in restaurants:
        shop, _ = Shop.objects.get_or_create(name=restaurant['name'])
        
        for menu_item in restaurant['menu']:
            food, _ = Food.objects.get_or_create(shop=shop, food_name=menu_item['food_name'], defaults={'price': menu_item['price']})
            
            active_discount = Discount.objects.filter(shop=shop, end_date__gt=now).first()
            if active_discount:
                discount_percentage = active_discount.discount_percentage
                end_date = active_discount.end_date
            else:
                discount_percentage = random.choice(discount_percentages)
                end_date = now + timedelta(days=random.randint(2, 3))
                Discount.objects.create(shop=shop, discount_percentage=discount_percentage, end_date=end_date)

            discounted_price = food.price * (Decimal(1) - Decimal(discount_percentage) / Decimal(100))
            discounted_foods.append({
                'food_name': food.food_name,
                'shop_name': shop.name,
                'original_price': food.price,
                'discount_percentage': discount_percentage,
                'discounted_price': round(discounted_price, 2),
                'valid_until': end_date
            })

    return discounted_foods

def assign_promotions(restaurants, number_of_promotions=5):
    promotions_json_path = os.path.join(os.path.dirname(__file__), 'dataPromotion', 'promotionJson.json')
    with open(promotions_json_path, 'r', encoding='utf-8') as file:
        promotion_data = json.load(file)
    available_promotions = promotion_data['promotions']
    
    now = timezone.now()
    active_promotions = Promotion.objects.filter(end_date__gt=now)

    if active_promotions.count() < number_of_promotions:
        selected_restaurants = random.sample(restaurants, number_of_promotions)
        
        for restaurant in selected_restaurants:
            promotion = random.choice(available_promotions)
            end_date = now + timedelta(days=random.randint(2, 3))
            shop, _ = Shop.objects.get_or_create(name=restaurant['name'])

            Promotion.objects.update_or_create(
                shop=shop,
                defaults={
                    'promotion_type': promotion['name'],
                    'description': promotion['description'],
                    'start_date': now,
                    'end_date': end_date
                }
            )

    active_promotions = Promotion.objects.filter(end_date__gt=now)
    return active_promotions

@login_required(login_url='authentication:login')
def promotions_and_discounts_list(request):
    user_favorites = request.GET.getlist('selected_shops')
    restaurants = load_restaurants()

    if user_favorites:
        filtered_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] in user_favorites]
        discounted_foods = assign_discounts(filtered_restaurants)
    else:
        selected_restaurants = random.sample(restaurants, 5) if len(restaurants) > 5 else restaurants
        all_discounted_foods = assign_discounts(selected_restaurants)
        discounted_foods = random.sample(all_discounted_foods, min(15, len(all_discounted_foods)))

    context = {
        'discounted_foods': discounted_foods,
        'promotions': assign_promotions(restaurants),
    }

    return render(request, 'promotions_discounts/list.html', context)

@login_required(login_url='authentication:login')
def delete_expired_discounts(request):
    if request.method == 'POST':
        today = timezone.now()
        expired_discounts = Discount.objects.filter(end_date__lt=today)
        deleted_count = expired_discounts.count()
        expired_discounts.delete()
        return JsonResponse({'deleted': deleted_count > 0, 'deleted_count': deleted_count})
    return JsonResponse({'deleted': False})

def import_data_from_json(request):
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for restaurant in data['restaurants']:
        shop, created = Shop.objects.get_or_create(name=restaurant['name'], defaults={
            'location': restaurant.get('location', '')
        })

        for menu_item in restaurant['menu']:
            Food.objects.get_or_create(
                shop=shop,
                food_name=menu_item['food_name'],
                price=menu_item['price']
            )

    return HttpResponse("Data imported successfully!")

@login_required(login_url='authentication:login')
def select_favorite_shops(request):
    form = FavoriteShopForm()
    context = {'form': form}
    return render(request, 'promotions_discounts/select_favorite_shops.html', context)
