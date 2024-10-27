from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FeaturedNews
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.core.files.storage import default_storage
from .models import Menu
from django.shortcuts import get_object_or_404
from usermanagement.models import Wishlist
import json  # Jangan lupa impor modul json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from .models import Restaurant, Menu
import json

from django.shortcuts import render


@csrf_exempt
@login_required(login_url='authentication:login')
def insert_restaurant_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            restaurant = Restaurant.objects.create(name=data['name'])
            for item in data['menu']:
                Menu.objects.create(
                    restaurant=restaurant,
                    food_name=item['food_name'],
                    price=item['price']
                )
            return JsonResponse({'message': 'Restaurant and menu added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def my_template_view(request):
    return render(request, 'restaurant_app/template.html')

@login_required(login_url='authentication:login')
def add_restaurant(request):
    if request.method == "POST":
        try:
            # Parsing JSON data dari request body
            data = json.loads(request.body)

            # Membuat restaurant baru
            restaurant = Restaurant.objects.create(name=data['name'])

            # Menambahkan menu items ke restaurant
            for item in data['menu']:
                Menu.objects.create(
                    restaurant=restaurant,
                    food_name=item['food_name'],
                    price=item['price']
                )
            
            # Mengembalikan response sukses
            return JsonResponse({'message': 'Restaurant and menu added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='authentication:login')
def show_main(request):
    # Ambil data restoran dari file JSON
    restaurants = load_restaurants()

    # Buat context yang berisi data user dan data restoran
    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login'),
        'restaurants': restaurants,  # Tambahkan data restoran ke context
    }

    # Render halaman main.html dengan data
    return render(request, 'main.html', context)

# @login_required(login_url='authentication:login')
def load_restaurants():
    # Gunakan double backslash
    json_path = 'datasets\datasets.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

def show_news_json(request):
    news = FeaturedNews.objects.all()
    return HttpResponse(serializers.serialize('json', news), content_type='application/json')

@login_required(login_url='authentication:login')
def create_news_ajax(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            content = request.POST.get('content')
            grand_title = request.POST.get('grand_title')
            author = request.POST.get('author')
            
            try:
                cooking_time = int(request.POST.get('cooking_time'))
                if cooking_time < 1:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Cooking time must be at least 1 minute'
                    }, status=400)
            except (ValueError, TypeError):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cooking time must be a valid number'
                }, status=400)

            try:
                calories = int(request.POST.get('calories'))
                if calories < 0:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Calories cannot be negative'
                    }, status=400)
            except (ValueError, TypeError):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Calories must be a valid number'
                }, status=400)

            icon_image = request.FILES.get('icon_image')
            grand_image = request.FILES.get('grand_image')

            if not all([title, content, grand_title, author, icon_image, grand_image]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'All fields are required'
                }, status=400)

            icon_path = default_storage.save(f'featured_news/icons/{icon_image.name}', icon_image)
            grand_path = default_storage.save(f'featured_news/images/{grand_image.name}', grand_image)

            news = FeaturedNews.objects.create(
                title=title,
                content=content,
                grand_title=grand_title,
                author=author,
                cooking_time=cooking_time,
                calories=calories,
                icon_image=icon_path,
                grand_image=grand_path,
                time_added=request.POST.get('time_added'),
            )

            return JsonResponse({
                'status': 'success',
                'message': 'News created successfully',
                'news': {
                    'id': news.id,
                    'title': news.title,
                    'content': news.content,
                    'grand_title': news.grand_title,
                    'author': news.author,
                    'cooking_time': news.cooking_time,
                    'calories': news.calories,
                    'time_added': news.time_added,
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

def delete_news(request, id):
    news = FeaturedNews.objects.get(pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='authentication:login')
def add_to_wishlist(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Menu, id=product_id)

        if Wishlist.objects.filter(user=user, product=product).exists():
            return JsonResponse({'status': 'error', 'message': 'Item already in wishlist'}, status=400)

        wishlist_item = Wishlist(user=user, product=product)
        wishlist_item.save()

        return JsonResponse({'status': 'success', 'message': 'Item added to wishlist'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

'''use this code to populate the database with dummy data, using shell
py manage.py shell -i python

from main.models import FeaturedNews

news_data = [
    {
        'title': 'Dummy News Title',
        'icon_image': 'featured_news/default.jpg',
        'grand_title': 'Dummy Grand Title',
        'content': 'This is a dummy content for the news.',
        'author': 'Author Name',
        'grand_image': 'featured_news/default.jpg',
        'cooking_time': 30,
        'calories': 250,
        'time_added': '2024-01-01',
    },
    {
        'title': 'Dummy News Title',
        'icon_image': 'featured_news/default.jpg',
        'grand_title': 'Dummy Grand Title',
        'content': 'This is a dummy content for the news.',
        'author': 'Author Name',
        'grand_image': 'featured_news/default.jpg',
        'cooking_time': 30,
        'calories': 250,
        'time_added': '2024-01-01',
    },
    {
        'title': 'Dummy News Title',
        'icon_image': 'featured_news/default.jpg',
        'grand_title': 'Dummy Grand Title',
        'content': 'This is a dummy content for the news.',
        'author': 'Author Name',
        'grand_image': 'featured_news/default.jpg',
        'cooking_time': 30,
        'calories': 250,
        'time_added': '2024-01-01',
    },
]

for news_item in news_data:
    FeaturedNews.objects.create(
        title=news_item['title'],
        icon_image=news_item['icon_image'],
        grand_title=news_item['grand_title'],
        content=news_item['content'],
        author=news_item['author'],
        grand_image=news_item['grand_image'],
        cooking_time=news_item['cooking_time'],
        calories=news_item['calories'],
        time_added=news_item['time_added']
    )
'''