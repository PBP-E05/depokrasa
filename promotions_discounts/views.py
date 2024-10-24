from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .models import Shop, Food, Discount, Promotion
from datetime import date, timedelta
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

    # Menentukan jumlah restoran yang akan mendapatkan diskon
    number_of_discounts = min(5, len(restaurants))  # Misalnya, 5 restoran secara acak atau sesuai jumlah restoran yang ada
    discount_percentages = [10, 15, 20, 25, 30]

    # Memilih restoran secara acak untuk diberikan diskon
    discounted_restaurants = random.sample(restaurants, number_of_discounts)

    # Menambahkan informasi diskon ke restoran yang dipilih
    for restaurant in discounted_restaurants:
        restaurant['discount_percentage'] = random.choice(discount_percentages)
        restaurant['discount_valid_until'] = (date.today() + timedelta(days=random.randint(2, 3))).strftime('%Y-%m-%d')

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

# View untuk menampilkan daftar promosi dan diskon
def promotions_and_discounts_list(request):
    # Load data dari JSON
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    restaurants = data['restaurants']

    # Tentukan jumlah restoran yang akan mendapatkan diskon
    number_of_discounts = min(5, len(restaurants))  # Contohnya 5 restoran atau sesuai jumlah restoran yang ada
    discount_percentages = [10, 15, 20, 25, 30]

    # Memilih restoran secara acak untuk diberikan diskon
    discounted_restaurants = random.sample(restaurants, number_of_discounts)

    # Membuat daftar makanan yang mendapatkan diskon
    discounted_foods = []
    for restaurant in discounted_restaurants:
        discount_percentage = random.choice(discount_percentages)
        valid_until = (date.today() + timedelta(days=random.randint(2, 3))).strftime('%Y-%m-%d')
        for menu_item in restaurant['menu']:
            discounted_price = menu_item['price'] - (menu_item['price'] * discount_percentage / 100)
            discounted_foods.append({
                'food_name': menu_item['food_name'],
                'shop_name': restaurant['name'],
                'original_price': menu_item['price'],
                'discount_percentage': discount_percentage,
                'discounted_price': round(discounted_price, 2),
                'valid_until': valid_until,
            })

    context = {
        'discounted_foods': discounted_foods,
    }

    return render(request, 'promotions_discounts/list.html', context)
