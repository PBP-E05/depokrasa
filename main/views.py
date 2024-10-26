from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FeaturedNews
from django.http import HttpResponse
from django.core import serializers
import json  # Jangan lupa impor modul json

# @login_required(login_url='authentication:login')
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

def load_restaurants():
    # Gunakan double backslash
    json_path = 'datasets\datasets.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['restaurants']

def show_news_json(request):
    news = FeaturedNews.objects.all()
    return HttpResponse(serializers.serialize('json', news), content_type='application/json')


'''use this code to populate the database with dummy data, using shell

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
        'comments': 100,
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
        'comments': 100,
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
        'comments': 100,
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
        comments=news_item['comments'],
        time_added=news_item['time_added']
    )
'''