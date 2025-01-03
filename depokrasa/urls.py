from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from promotions_discounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('user/', include('usermanagement.urls', namespace='usermanagement')),
    path('promotions/', include('promotions_discounts.urls', namespace='promotions_discounts')),
    path('articles/', include('articles.urls', namespace='articles')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)