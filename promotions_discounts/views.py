from django.shortcuts import render
from .models import Discount, Promotion

def promotions_and_discounts_list(request):
    discounts = Discount.objects.all()
    promotions = Promotion.objects.all()
    context = {
        'discounts': discounts,
        'promotions': promotions,
    }
    return render(request, 'promotions_discounts/list.html', context)
