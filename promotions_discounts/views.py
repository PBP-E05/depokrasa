from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from .models import Shop, Food, Discount, Promotion, UserFavoriteShop
from datetime import date, timedelta, datetime
from django.utils import timezone
import random

# View untuk menampilkan halaman utama
def load_restaurants():
    # Membaca file JSON
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

@login_required(login_url='authentication:login')
def show_main(request):
    # Mengambil data restoran dari file JSON
    restaurants = load_restaurants()

    # Mengambil daftar restoran favorit user
    user_favorites = UserFavoriteShop.objects.filter(user=request.user)
    favorite_shops = [fav.shop.name for fav in user_favorites]

    # Menentukan jumlah restoran yang akan mendapatkan diskon
    number_of_discounts = min(5, len(restaurants))  # Misalnya, 5 restoran secara acak atau sesuai jumlah restoran yang ada
    discount_percentages = [10, 15, 20, 25, 30]

    # Memilih restoran secara acak untuk diberikan diskon, dengan prioritas pada restoran favorit
    favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] in favorite_shops]
    non_favorite_restaurants = [restaurant for restaurant in restaurants if restaurant['name'] not in favorite_shops]

    discounted_restaurants = random.sample(favorite_restaurants, min(len(favorite_restaurants), number_of_discounts))
    if len(discounted_restaurants) < number_of_discounts:
        remaining_discounts = number_of_discounts - len(discounted_restaurants)
        discounted_restaurants += random.sample(non_favorite_restaurants, remaining_discounts)

    # Menambahkan informasi diskon ke restoran yang dipilih
    for restaurant in discounted_restaurants:
        restaurant['discount_percentage'] = random.choice(discount_percentages)
        restaurant['discount_valid_until'] = (datetime.now() + timedelta(days=random.randint(2, 3))).strftime('%Y-%m-%d %H:%M:%S')

    # Buat konteks untuk halaman template
    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login'),
        'restaurants': restaurants,
    }

    # Render halaman dengan data
    return render(request, 'main.html', context)

# View untuk mengimpor data dari JSON ke dalam database
def import_data_from_json(request):
    # Membaca file JSON
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Loop melalui data dan masukkan ke dalam database
    for restaurant in data['restaurants']:
        # Buat atau dapatkan objek Shop
        shop, created = Shop.objects.get_or_create(name=restaurant['name'], defaults={
            'location': restaurant.get('location', '')
        })

        # Buat entri makanan untuk setiap restoran
        for menu_item in restaurant['menu']:
            Food.objects.get_or_create(
                shop=shop,
                food_name=menu_item['food_name'],
                price=menu_item['price']
            )

    return HttpResponse("Data imported successfully!")

@login_required(login_url='authentication:login')
def promotions_and_discounts_list(request):
    today = datetime.now()  # Use naive datetime

    # Hapus diskon yang sudah kedaluwarsa
    Discount.objects.filter(end_date__lt=today).delete()

    # Load data dari JSON
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    restaurants = data['restaurants']

    # Get the user's favorite shops
    user_favorites = UserFavoriteShop.objects.filter(user=request.user)
    favorite_shops = [fav.shop.name for fav in user_favorites]

    # Create new discounts if needed
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

        # Save new discount to the database
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

    context = {
        'discounted_foods': discounted_foods,
    }

    return render(request, 'promotions_discounts/list.html', context)

@login_required(login_url='authentication:login')
def delete_expired_discounts(request):
    if request.method == 'POST':
        today = datetime.now()
        expired_discounts = Discount.objects.filter(end_date__lt=today)
        deleted_count = expired_discounts.count()
        expired_discounts.delete()
        return JsonResponse({'deleted': deleted_count > 0, 'deleted_count': deleted_count})
    return JsonResponse({'deleted': False})

