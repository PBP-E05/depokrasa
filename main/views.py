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
import os;

@csrf_exempt
@login_required(login_url='authentication:login_user')
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

@login_required(login_url='authentication:login_user')
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



@login_required(login_url='authentication:login_user')
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

def get_restaurants(request):
    # Get all restaurants
    json_path = 'datasets/datasets.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return JsonResponse(data['restaurants'], safe=False)

# @login_required(login_url='authentication:login')
def load_restaurants():
    # Gunakan double backslash
    json_path = 'datasets/datasets.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

def show_news_json(request):
    news = FeaturedNews.objects.all()
    return HttpResponse(serializers.serialize('json', news), content_type='application/json')

@csrf_exempt
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

@csrf_exempt
def create_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body).get('fields')
            title = data.get('title')
            content = data.get('content')
            grand_title = data.get('grand_title')
            author = data.get('author')
            cooking_time = data.get('cooking_time')
            calories = data.get('calories')
            icon_image = data.get('icon_image')  # Assuming these are URLs or base64 strings
            grand_image = data.get('grand_image')  # Assuming these are URLs or base64 strings

            if not all([title, content, grand_title, author]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Title, content, grand title, and author are required'
                }, status=400)

            time_added = data.get('time_added')
            created_at = data.get('created_at')
            updated_at = data.get('updated_at')

            if time_added:
                time_added = datetime.strptime(time_added, '%Y-%m-%dT%H:%M:%S.%f')
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%f')
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f')

            news = FeaturedNews.objects.create(
                title=title,
                content=content,
                grand_title=grand_title,
                author=author,
                cooking_time=cooking_time,
                calories=calories,
                icon_image=icon_image,
                grand_image=grand_image,
                time_added=time_added,
                created_at=created_at,
                updated_at=updated_at,
            )

            return JsonResponse({
                'status': 'success',
                'message': 'News created successfully',
                'news_id': news.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
        except KeyError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Missing field: {str(e)}'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)

@csrf_exempt
def edit_news(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body).get('fields')
            news = get_object_or_404(FeaturedNews, pk=id)

            news.title = data.get('title', news.title)
            news.content = data.get('content', news.content)
            news.grand_title = data.get('grand_title', news.grand_title)
            news.author = data.get('author', news.author)
            news.cooking_time = data.get('cooking_time', news.cooking_time)
            news.calories = data.get('calories', news.calories)
            news.icon_image = data.get('icon_image', news.icon_image)
            news.grand_image = data.get('grand_image', news.grand_image)
            news.time_added = data.get('time_added', news.time_added)
            news.save()

            return JsonResponse({
                'status': 'success',
                'message': 'News updated successfully',
                'news_id': news.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
        except KeyError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Missing field: {str(e)}'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)
    
@csrf_exempt
def delete_news(request, id):
    if request.method == 'DELETE':
        try:
            news = get_object_or_404(FeaturedNews, pk=id)
            news.delete()
            return JsonResponse({'status': 'success', 'message': 'News deleted successfully'}, status=200)
        except FeaturedNews.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'News not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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