from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from .models import Shop, Food, Discount, UserFavoriteShop
from datetime import datetime, timedelta
import os
import random

# Function to load restaurants data from JSON
def load_restaurants():
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

@login_required(login_url='authentication:login')
def show_main(request):
    # Load restaurants from JSON
    restaurants = load_restaurants()

    # Get user's favorite shops
    user_favorites = UserFavoriteShop.objects.filter(user=request.user)
    favorite_shops = [fav.shop.name for fav in user_favorites]

    # Determine the number of discounts to apply
    number_of_discounts = min(5, len(restaurants))
    discount_percentages = [10, 15, 20, 25, 30]

    # Select restaurants for discount (prioritizing favorites)
    favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] in favorite_shops]
    non_favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] not in favorite_shops]

    discounted_restaurants = random.sample(favorite_restaurants, min(len(favorite_restaurants), number_of_discounts))
    if len(discounted_restaurants) < number_of_discounts:
        remaining_discounts = number_of_discounts - len(discounted_restaurants)
        discounted_restaurants += random.sample(non_favorite_restaurants, remaining_discounts)

    # Add discount info to selected restaurants
    for restaurant in discounted_restaurants:
        restaurant['discount_percentage'] = random.choice(discount_percentages)
        restaurant['discount_valid_until'] = (datetime.now() + timedelta(days=random.randint(2, 3))).strftime('%Y-%m-%d %H:%M:%S')

    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login'),
        'restaurants': restaurants,
    }

    return render(request, 'main.html', context)

# Function to import data into the database from JSON
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

# View to display promotions and discounts list
@login_required(login_url='authentication:login')
def promotions_and_discounts_list(request):
    today = datetime.now()

    # Remove expired discounts
    Discount.objects.filter(end_date__lt=today).delete()

    # Load restaurant data
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    restaurants = data['restaurants']

    # Get user's favorite shops
    user_favorites = UserFavoriteShop.objects.filter(user=request.user)
    favorite_shops = [fav.shop.name for fav in user_favorites]

    # Apply random discounts
    number_of_discounts = min(5, len(restaurants))
    discount_percentages = [10, 15, 20, 25, 30]
    favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] in favorite_shops]
    non_favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] not in favorite_shops]

    discounted_restaurants = random.sample(favorite_restaurants, min(len(favorite_restaurants), number_of_discounts))
    if len(discounted_restaurants) < number_of_discounts:
        remaining_discounts = number_of_discounts - len(discounted_restaurants)
        discounted_restaurants += random.sample(non_favorite_restaurants, remaining_discounts)

    discounted_foods = []

    for restaurant in discounted_restaurants:
        discount_percentage = random.choice(discount_percentages)
        end_date = datetime.now() + timedelta(days=random.randint(2, 3))

        shop, _ = Shop.objects.get_or_create(name=restaurant['name'])
        discount = Discount.objects.create(
            shop=shop,
            discount_percentage=discount_percentage,
            end_date=end_date
        )

        for menu_item in restaurant['menu']:
            discounted_price = menu_item['price'] - (menu_item['price'] * discount.discount_percentage / 100)
            discounted_foods.append({
                'food_name': menu_item['food_name'],
                'shop_name': restaurant['name'],
                'original_price': menu_item['price'],
                'discount_percentage': discount.discount_percentage,
                'discounted_price': round(discounted_price, 2),
                'valid_until': discount.end_date.isoformat(),
            })

    # Load promotions from JSON
    promotions_json_path = os.path.join(os.path.dirname(__file__), 'dataPromotion', 'promotionJson.json')
    with open(promotions_json_path, 'r', encoding='utf-8') as file:
        promotion_data = json.load(file)
    available_promotions = promotion_data['promotions']

    # Assign random promotions to selected restaurants
    number_of_promotions = min(5, len(restaurants))
    promoted_restaurants = random.sample(restaurants, number_of_promotions)

    promotions_list = []
    for restaurant in promoted_restaurants:
        promotion = random.choice(available_promotions)
        promotions_list.append({
            'restaurant_name': restaurant['name'],
            'promotion_name': promotion['name'],
            'promotion_description': promotion['description']
        })

    context = {
        'discounted_foods': discounted_foods,
        'promotions': promotions_list,
    }

    return render(request, 'promotions_discounts/list.html', context)

# Function to delete expired discounts
@login_required(login_url='authentication:login')
def delete_expired_discounts(request):
    if request.method == 'POST':
        today = datetime.now()
        expired_discounts = Discount.objects.filter(end_date__lt=today)
        deleted_count = expired_discounts.count()
        expired_discounts.delete()
        return JsonResponse({'deleted': deleted_count > 0, 'deleted_count': deleted_count})
    return JsonResponse({'deleted': False})
