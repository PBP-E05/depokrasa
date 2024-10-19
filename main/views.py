from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication:login')
def show_main(request):
    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login')
    }

    return render(request, 'main.html', context)