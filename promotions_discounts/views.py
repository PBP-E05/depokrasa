from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from .models import Shop, Food, Discount, UserFavoriteShop
from .forms import FavoriteShopForm
from datetime import datetime, timedelta
import os
import random

# Function to load restaurants data from JSON
def load_restaurants():
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

# Helper function to assign discounts to restaurants, with priority for favorite shops
def assign_discounts(user, restaurants, number_of_discounts=5):
    discount_percentages = [10, 15, 20, 25, 30]
    
    # Get user's favorite shops
    user_favorites = UserFavoriteShop.objects.filter(user=user)
    favorite_shops = [fav.shop.name for fav in user_favorites]
    
    # Boost favorite restaurants in selection pool
    boosted_restaurants = []
    for restaurant in restaurants:
        boosted_restaurants.append(restaurant)
        if restaurant['name'] in favorite_shops:
            boosted_restaurants.extend([restaurant] * 3)  # Add 30% more weight by repeating

    # Select random restaurants with boosted favorites
    discounted_restaurants = random.sample(boosted_restaurants, min(number_of_discounts, len(restaurants)))

    # Apply discount info to selected restaurants
    discounted_foods = []
    for restaurant in discounted_restaurants:
        discount_percentage = random.choice(discount_percentages)
        end_date = datetime.now() + timedelta(days=random.randint(2, 3))
        shop, _ = Shop.objects.get_or_create(name=restaurant['name'])

        # Create the discount entry
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

    return discounted_foods

# Helper function to assign promotions to restaurants
def assign_promotions(restaurants, number_of_promotions=5):
    promotions_json_path = os.path.join(os.path.dirname(__file__), 'dataPromotion', 'promotionJson.json')
    with open(promotions_json_path, 'r', encoding='utf-8') as file:
        promotion_data = json.load(file)
    available_promotions = promotion_data['promotions']

    promoted_restaurants = random.sample(restaurants, number_of_promotions)
    promotions_list = []
    for restaurant in promoted_restaurants:
        promotion = random.choice(available_promotions)
        promotions_list.append({
            'restaurant_name': restaurant['name'],
            'promotion_name': promotion['name'],
            'promotion_description': promotion['description']
        })

    return promotions_list

@login_required
def show_main(request):
    # Load restaurants from JSON
    restaurants = load_restaurants()

    # Assign discounts with preference for user's favorite shops
    discounted_foods = assign_discounts(request.user, restaurants)

    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login'),
        'restaurants': restaurants,
        'discounted_foods': discounted_foods,
    }

    return render(request, 'main.html', context)

# View to import data into the database from JSON
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
@login_required
def promotions_and_discounts_list(request):
    today = datetime.now()

    # Remove expired discounts
    Discount.objects.filter(end_date__lt=today).delete()

    # Load restaurant data
    restaurants = load_restaurants()

    # Assign discounts and promotions
    discounted_foods = assign_discounts(request.user, restaurants)
    promotions_list = assign_promotions(restaurants)

    context = {
        'discounted_foods': discounted_foods,
        'promotions': promotions_list,
    }

    return render(request, 'promotions_discounts/list.html', context)

# View for users to select favorite shops and assign weights
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

# View to delete expired discounts
@login_required
def delete_expired_discounts(request):
    if request.method == 'POST':
        today = datetime.now()
        expired_discounts = Discount.objects.filter(end_date__lt=today)
        deleted_count = expired_discounts.count()
        expired_discounts.delete()
        return JsonResponse({'deleted': deleted_count > 0, 'deleted_count': deleted_count})
    return JsonResponse({'deleted': False})
