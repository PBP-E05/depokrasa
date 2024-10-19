import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from usermanagement.models import Wishlist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='authentication:login')
def show_wishlist(request):
    # wishlists = Wishlist.objects.filter(user=request.user)
    wishlists = Wishlist.objects.all()
    context = {
        'wishlists': wishlists,
        'last_login': request.COOKIES.get('last_login')
    }
    return render(request, 'wishlist.html', context)

@csrf_exempt
@require_POST
def add_wishlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        user = request.user
        wishlist = Wishlist(name=name, description=description, price=price, image=image, user=user)
        wishlist.save()
        return redirect('usermanagement:wishlist')
    
def delete_wishlist(request, id):
    wishlist = Wishlist.objects.get(id=id)
    wishlist.delete()
    return redirect('usermanagement:wishlist')

def clear_wishlist(request):
    wishlists = Wishlist.objects.all()
    wishlists.delete()
    return redirect('usermanagement:wishlist')