from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from .models import Shop, Food, Discount, Promotion, UserFavoriteShop
from .forms import FavoriteShopForm
from datetime import datetime, timedelta
from django.utils import timezone
import os
import random
from decimal import Decimal

# Load restaurant data from JSON
def load_restaurants():
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

def assign_discounts(user, restaurants, max_restaurants=5, max_foods=15):
    discount_percentages = [10, 15, 20, 25, 30]
    now = timezone.now()
    discounted_foods = []

    # Limit the number of restaurants to process
    selected_restaurants = random.sample(restaurants, min(max_restaurants, len(restaurants)))

    for restaurant in selected_restaurants:
        shop, _ = Shop.objects.get_or_create(name=restaurant['name'])
        
        # Process each food item in the restaurant up to max_foods
        for menu_item in restaurant['menu'][:max_foods]:
            food, _ = Food.objects.get_or_create(shop=shop, food_name=menu_item['food_name'], defaults={'price': menu_item['price']})

            # Check if there’s an active discount for this specific food item
            active_discount = Discount.objects.filter(shop=shop, end_date__gt=now).first()

            if active_discount:
                # Reuse existing discount for this food
                discount_percentage = active_discount.discount_percentage
                end_date = active_discount.end_date
            else:
                # Create a new discount for this food
                discount_percentage = random.choice(discount_percentages)
                end_date = now + timedelta(days=random.randint(2, 3))
                Discount.objects.create(
                    shop=shop,
                    discount_percentage=discount_percentage,
                    end_date=end_date
                )

            # Calculate discounted price and add to list
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

# Helper function to assign and persist promotions
def assign_promotions(restaurants, number_of_promotions=5):
    # Load promotion data from JSON file
    promotions_json_path = os.path.join(os.path.dirname(__file__), 'dataPromotion', 'promotionJson.json')
    with open(promotions_json_path, 'r', encoding='utf-8') as file:
        promotion_data = json.load(file)
    available_promotions = promotion_data['promotions']
    
    # Get current time and filter active promotions
    now = timezone.now()
    active_promotions = Promotion.objects.filter(end_date__gt=now)

    # Create new promotions if needed
    if active_promotions.count() < number_of_promotions:
        selected_restaurants = random.sample(restaurants, number_of_promotions)
        
        for restaurant in selected_restaurants:
            promotion = random.choice(available_promotions)
            end_date = now + timedelta(days=random.randint(2, 3))
            shop, _ = Shop.objects.get_or_create(name=restaurant['name'])

            # Persist promotion
            Promotion.objects.update_or_create(
                shop=shop,
                defaults={
                    'promotion_type': promotion['name'],
                    'description': promotion['description'],
                    'start_date': now,
                    'end_date': end_date
                }
            )

    # Retrieve updated active promotions
    active_promotions = Promotion.objects.filter(end_date__gt=now)
    return active_promotions

@login_required
def show_main(request):
    # Load restaurants from JSON
    restaurants = load_restaurants()

    # Assign discounts
    discounted_foods = assign_discounts(request.user, restaurants)

    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login'),
        'restaurants': restaurants,
        'discounted_foods': discounted_foods,
    }

    return render(request, 'main.html', context)

@login_required
def promotions_and_discounts_list(request):
    # Load restaurant data
    restaurants = load_restaurants()

    # Get active discounts and promotions
    discounted_foods = assign_discounts(request.user, restaurants)
    promotions_list = assign_promotions(restaurants)

    context = {
        'discounted_foods': discounted_foods,
        'promotions': promotions_list,
    }

    return render(request, 'promotions_discounts/list.html', context)

# View to delete expired discounts
@login_required
def delete_expired_discounts(request):
    if request.method == 'POST':
        today = timezone.now()
        expired_discounts = Discount.objects.filter(end_date__lt=today)
        deleted_count = expired_discounts.count()
        expired_discounts.delete()
        return JsonResponse({'deleted': deleted_count > 0, 'deleted_count': deleted_count})
    return JsonResponse({'deleted': False})

# Import data from JSON to database
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

# View for selecting favorite shops
@login_required
def select_favorite_shops(request):
    if request.method == 'POST':
        form = FavoriteShopForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('promotions_discounts:promotions_and_discounts_list')
    else:
        form = FavoriteShopForm()

    return render(request, 'promotions_discounts/select_favorite_shops.html', {'form': form})
