from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from decimal import Decimal
import json
import random
import os

from .models import Restaurant, Menu, Discount, Promotion, UserFavoriteRestaurant

def import_data_from_json(request):
    """
    Mengimpor data restoran dan menu dari file JSON ke database.
    Diskon dan Promosi dikelola melalui admin, jadi tidak di-generate dari sini.
    """
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for restaurant_data in data['restaurants']:
        restaurant, created = Restaurant.objects.get_or_create(
            name=restaurant_data['name'], 
        )

        for menu_item in restaurant_data['menu']:
            Menu.objects.get_or_create(
                restaurant=restaurant,
                food_name=menu_item['food_name'],
                defaults={'price': menu_item['price']}
            )

    return HttpResponse("Data imported successfully!")

def get_active_discounts(restaurants):
    """
    Mengambil diskon yang aktif untuk restoran yang diberikan.
    Diskon aktif jika now <= start_time + duration.
    """
    now = timezone.now()
    # Filter discount yang menu_item__restaurant terdapat di daftar restaurants
    discounts = Discount.objects.filter(menu_item__restaurant__in=restaurants)
    active_discounts = []
    for d in discounts:
        end_time = d.start_time + d.duration
        if now <= end_time:
            active_discounts.append(d)
    return active_discounts

def get_active_promotions(restaurants):
    """
    Mengambil promosi yang masih aktif (end_date > now) untuk restoran yang diberikan.
    """
    now = timezone.now()
    return Promotion.objects.filter(restaurant__in=restaurants, end_date__gt=now)

@login_required(login_url='authentication:login')
def promotions_and_discounts_list(request):
    """
    Menampilkan daftar diskon dan promosi.  
    Jika user telah memilih restoran favorit (via GET param), maka hanya restoran tersebut yang ditampilkan.
    Jika belum memilih, tampilkan pesan untuk memilih restoran.
    Jika tidak ada diskon/promosi, tampilkan pesan bahwa saat ini tidak tersedia.
    """

    selected_restaurant_names = request.GET.getlist('selected_restaurants')

    if not selected_restaurant_names:
        restaurants = Restaurant.objects.all()
    else:
        restaurants = Restaurant.objects.filter(name__in=selected_restaurant_names)
    
    # Ambil diskon yang aktif
    active_discounts = get_active_discounts(restaurants)[:6]
    discounted_foods = []
    for d in active_discounts:
        discounted_foods.append({
            'food_name': d.menu_item.food_name,
            'restaurant_name': d.menu_item.restaurant.name,
            'original_price': d.original_price,
            'discount_percentage': d.discount_percentage,
            'discounted_price': d.discounted_price,
            'start_time': d.start_time.isoformat(),  # Format ISO 8601
            'duration_seconds': int(d.duration.total_seconds()),  # Konversi ke detik
        })

    # Ambil promosi yang aktif
    active_promotions = get_active_promotions(restaurants)[:6]

    # Jika tidak ada diskon dan tidak ada promosi
    if not discounted_foods and not active_promotions:
        return render(request, 'promotions_discounts/list.html', {
            'discounted_foods': [],
            'promotions': [],
            'message': "Maaf, saat ini tidak ada diskon atau promosi."
        })

    # Jika tidak ada diskon
    if not discounted_foods and active_promotions:
        return render(request, 'promotions_discounts/list.html', {
            'discounted_foods': [],
            'promotions': active_promotions,
            'message': "Maaf, tidak ada diskon yang tersedia."
        })

    # Jika tidak ada promosi
    if discounted_foods and not active_promotions:
        return render(request, 'promotions_discounts/list.html', {
            'discounted_foods': discounted_foods,
            'promotions': [],
            'message': "Maaf, tidak ada promosi yang tersedia."
        })

    return render(request, 'promotions_discounts/list.html', {
        'discounted_foods': discounted_foods,
        'promotions': active_promotions,
        'message': ""
    })

@login_required(login_url='authentication:login')
def delete_expired_discounts(request):
    """
    Menghapus diskon dan promosi yang telah kedaluwarsa.
    Diskon kedaluwarsa jika now > start_time + duration.
    Promosi kedaluwarsa jika now > end_date.
    """
    if request.method == 'POST':
        now = timezone.now()
        
        # Hapus diskon yang expired
        # Diskon expired jika start_time + duration < now
        # Gunakan annotate untuk menghitung end_time: end_time = start_time + duration
        # Karena DurationField tidak bisa langsung dalam filter, kita bisa filter secara manual
        expired_discounts = []
        for discount in Discount.objects.all():
            if discount.start_time + discount.duration < now:
                expired_discounts.append(discount.id)
        
        deleted_discount_count = Discount.objects.filter(id__in=expired_discounts).delete()[0]

        # Hapus promosi yang expired
        expired_promotions = Promotion.objects.filter(end_date__lt=now)
        deleted_promotion_count = expired_promotions.count()
        expired_promotions.delete()

        return JsonResponse({
            'deleted_discounts': deleted_discount_count > 0,
            'deleted_count_discounts': deleted_discount_count,
            'deleted_promotions': deleted_promotion_count > 0,
            'deleted_count_promotions': deleted_promotion_count
        })
    return JsonResponse({'deleted': False})

@login_required(login_url='authentication:login')
def select_favorite_restaurants(request):
    """
    View ini untuk memilih restoran favorit, mungkin dengan form atau checkbox.
    Setelah dipilih, user akan diarahkan ke promotions_and_discounts_list 
    dengan query param terpilih.
    """
    # Misal kita menampilkan semua restoran yang ada untuk dipilih.
    restaurants = Restaurant.objects.all()
    if request.method == 'POST':
        selected = request.POST.getlist('restaurants')
        if selected:
            query_param = "&".join([f"selected_restaurants={name}" for name in selected])
            return redirect(f'/promotions-and-discounts/?{query_param}')
        else:
            # Jika tidak ada yang dipilih
            return render(request, 'promotions_discounts/select_favorite_restaurants.html', {
                'restaurants': restaurants,
                'message': "Anda belum memilih restoran apapun."
            })
    return render(request, 'promotions_discounts/select_favorite_restaurants.html', {
        'restaurants': restaurants
    })
