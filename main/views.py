from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication:login')
def show_main(request):
    # user = request.user
    # user_profile = user.userprofile 
    # print(f'User: {user}')
    # for attr, value in user.__dict__.items():
    #     print(f'{attr}: {value}')

    # print(f'UserProfile: {user_profile}')
    # for attr, value in user_profile.__dict__.items():
    #     print(f'{attr}: {value}')

    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login')
    }

    return render(request, 'main.html', context)