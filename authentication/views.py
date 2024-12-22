import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.middleware.csrf import get_token
from .models import UserProfile

#for web login
def login_user(request):
   if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password.')
   else:
        form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

#for web register
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                auth_login(request, user)
            return redirect('authentication:login_user')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

#for web logout
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login_user'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    csrf_token = get_token(request)


    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "isAdmin": user.is_staff,
                "csrfToken": csrf_token
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def get_profile(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                return JsonResponse({
                    "username": user.username,
                    "email": profile.email,
                    "profile_picture": profile.profile_picture.url,
                    "status": True,
                    "message": "Profile retrieved successfully."
                }, status=200)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "Profile does not exist."
                }, status=404)
        else:
            return JsonResponse({
                "status": False,
                "message": "User is not authenticated."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            data = json.loads(request.body)
            email = data.get('email')
            profile_picture = data.get('profile_picture')

            try:
                profile = UserProfile.objects.get(user=user)
                if email:
                    profile.email = email
                if profile_picture:
                    profile.profile_picture = profile_picture
                profile.save()
                return JsonResponse({
                    "status": True,
                    "message": "Profile updated successfully."
                }, status=200)
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "Profile does not exist."
                }, status=404)
        else:
            return JsonResponse({
                "status": False,
                "message": "User is not authenticated."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

def get_restaurants(request):
    # Get all restaurants
    json_path = 'datasets\datasets.json'

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return JsonResponse(data['restaurants'], safe=False)