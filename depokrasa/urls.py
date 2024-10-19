from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('user/', include('usermanagement.urls', namespace='usermanagement')),
    path('', include('main.urls')),
]
