from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
