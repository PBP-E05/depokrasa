from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import json
import os
from django.core.serializers.json import DjangoJSONEncoder

from .models import Restaurant, Menu, Discount, Promotion, UserFavoriteRestaurant

def get_restaurant_names(request):
    """
    Mengembalikan daftar nama restoran dalam format JSON.
    """
    restaurants = Restaurant.objects.values_list('name', flat=True)
    return JsonResponse(list(restaurants), safe=False)

def discounts_list(request):
    """
    Endpoint untuk mendapatkan daftar diskon dalam format JSON.
    """
    discounts = Discount.objects.all()
    serialized_data = serialize_discounts(discounts)
    return JsonResponse(json.loads(serialized_data), safe=False)

def promotions_list(request):
    """
    Endpoint untuk mendapatkan daftar promosi dalam format JSON.
    """
    promotions = Promotion.objects.all()
    serialized_data = serialize_promotions(promotions)
    return JsonResponse(json.loads(serialized_data), safe=False)

def serialize_discounts(discounts):
    """
    Serialize queryset Discount menjadi JSON.
    """
    serialized_data = []
    for discount in discounts:
        serialized_data.append({
            'id': discount.id,
            'food_name': discount.menu_item.food_name,
            'restaurant_name': discount.menu_item.restaurant.name,
            'original_price': float(discount.original_price),
            'discount_percentage': float(discount.discount_percentage),
            'discounted_price': float(discount.discounted_price),
            'start_time': discount.start_time.isoformat(),
            'end_time': discount.end_time.isoformat(),
        })
    return json.dumps(serialized_data, cls=DjangoJSONEncoder)

def serialize_promotions(promotions):
    """
    Serialize queryset Promotion menjadi JSON.
    """
    serialized_data = []
    for promotion in promotions:
        serialized_data.append({
            'id': promotion.id,
            'restaurant_name': promotion.restaurant.name,
            'promotion_type': promotion.promotion_type,
            'description': promotion.description,
            'start_date': promotion.start_date.isoformat(),
            'end_date': promotion.end_date.isoformat(),
        })
    return json.dumps(serialized_data, cls=DjangoJSONEncoder)

def import_data_from_json(request):
    """
    Mengimpor data restoran dan menu dari file JSON ke database.
    Diskon dan Promosi dikelola melalui admin, jadi tidak di-generate dari sini.
    Tidak menggunakan field 'location' karena model Restaurant tidak memilikinya.
    """
    json_path = 'datasets/datasets.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for restaurant_data in data['restaurants']:
        # Buat atau dapatkan Restaurant hanya dengan 'name', tanpa location
        restaurant, created = Restaurant.objects.get_or_create(
            name=restaurant_data['name']
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
    Mengambil diskon yang aktif untuk restoran.
    Diskon aktif jika now <= start_time + duration.
    """
    now = timezone.now()
    discounts = Discount.objects.filter(menu_item__restaurant__in=restaurants)
    active_discounts = []
    for d in discounts:
        end_time = d.start_time + d.duration
        if now <= end_time:
            active_discounts.append(d)
    return active_discounts

def get_active_promotions(restaurants):
    """
    Mengambil promosi yang masih aktif (end_date > now) untuk restoran.
    """
    now = timezone.now()
    return Promotion.objects.filter(restaurant__in=restaurants, end_date__gt=now)

def promotions_and_discounts_list(request):
    """
    Menampilkan daftar diskon dan promosi dalam format HTML.
    Menggunakan nama restoran dari model Restaurant (tanpa location).
    Jika user telah memilih restoran favorit, tampilkan hanya untuk restoran tersebut.
    Jika tidak, tampilkan semua.
    Batasi diskon dan promosi hingga 6 item.
    """
    selected_restaurant_names = request.GET.getlist('selected_restaurants')

    if not selected_restaurant_names:
        # Jika tidak ada filter restoran, tampilkan semua restoran
        restaurants = Restaurant.objects.all()
    else:
        restaurants = Restaurant.objects.filter(name__in=selected_restaurant_names)
    
    # Ambil diskon aktif (maksimal 6)
    active_discounts = get_active_discounts(restaurants)[:6]
    discounted_foods = []
    for d in active_discounts:
        discounted_foods.append({
            'food_name': d.menu_item.food_name,
            'restaurant_name': d.menu_item.restaurant.name,
            'original_price': d.original_price,
            'discount_percentage': d.discount_percentage,
            'discounted_price': d.discounted_price,
            'start_time': d.start_time.isoformat(),
            'duration_seconds': int(d.duration.total_seconds()),
        })

    # Ambil promosi aktif (maksimal 6)
    active_promotions = get_active_promotions(restaurants)[:6]

    # Logika pesan dan pengembalian template
    if not discounted_foods and not active_promotions:
        return render(request, 'promotions_discounts/list.html', {
            'discounted_foods': [],
            'promotions': [],
            'message': "Maaf, saat ini tidak ada diskon atau promosi."
        })

    if not discounted_foods and active_promotions:
        return render(request, 'promotions_discounts/list.html', {
            'discounted_foods': [],
            'promotions': active_promotions,
            'message': "Maaf, tidak ada diskon yang tersedia."
        })

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

def delete_expired_discounts(request):
    """
    Menghapus diskon dan promosi yang telah kadaluwarsa.
    Dikembalikan dalam format JSON.
    """
    if request.method == 'POST':
        now = timezone.now()
        
        # Hapus diskon yang expired
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

def select_favorite_restaurants(request):
    """
    Memilih restoran favorit. Karena model Restaurant tidak punya location,
    kita hanya tampilkan nama restoran.
    """
    restaurants = Restaurant.objects.all()
    if request.method == 'POST':
        selected = request.POST.getlist('restaurants')
        if selected:
            query_param = "&".join([f"selected_restaurants={name}" for name in selected])
            return redirect(f'/promotions-and-discounts/?{query_param}')
        else:
            # Tidak memilih apapun
            return render(request, 'promotions_discounts/select_favorite_restaurants.html', {
                'restaurants': restaurants,
                'message': "Anda belum memilih restoran apapun."
            })
    return render(request, 'promotions_discounts/select_favorite_restaurants.html', {
        'restaurants': restaurants
    })
