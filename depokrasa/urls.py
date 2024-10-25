from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from promotions_discounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('user/', include('usermanagement.urls', namespace='usermanagement')),
    path('', include('main.urls')),
    path('promotions/', include('promotions_discounts.urls', namespace='promotions_discounts')),
    path('select_favorites/', views.select_favorite_shops, name='select_favorite_shops'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)