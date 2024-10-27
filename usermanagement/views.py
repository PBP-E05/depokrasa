from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usermanagement.models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import EditProfileForm, EditUserProfileForm
from .utils import generate_random_color
from authentication.models import UserProfile
import datetime

@login_required(login_url='authentication:login')
def show_wishlist(request):
    # wishlists = Wishlist.objects.filter(user=request.user)
    wishlists = Wishlist.objects.all()
    context = {
        'wishlists': wishlists,
        'last_login': request.COOKIES.get('last_login'),
        'date_time': datetime.datetime.now().strftime('%d/%m'),
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='authentication:login')
def edit_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = EditUserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and profile_form.is_valid():
            profile_form.save()
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('usermanagement:profile')
        else:
            print(form.errors)
            print(profile_form.errors)
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=user_profile)
    
    # print('woiii', profile_form)
    context = {
        'form': form,
        'profile_form': profile_form,
        'random_color': generate_random_color(),
        'random_color_2': generate_random_color(),
    }
    return render(request, 'profile.html', context)

@csrf_exempt
@require_POST
@login_required(login_url='authentication:login')
def add_wishlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        # image = request.FILES.get('image')
        user = request.user
        wishlist = Wishlist(name=name, description=description, price=price, user=user)
        wishlist.save()
        return redirect('usermanagement:wishlist')
    
@login_required(login_url='authentication:login')
def delete_wishlist(request, id):
    wishlist = Wishlist.objects.get(id=id)
    wishlist.delete()
    return redirect('usermanagement:wishlist')

@login_required(login_url='authentication:login')
def clear_wishlist(request):
    wishlists = Wishlist.objects.all()
    wishlists.delete()
    return redirect('usermanagement:wishlist')