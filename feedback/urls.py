from django.urls import path
from .views import faq_page

app_name = 'feedback'

urlpatterns = [
    path('faq/', faq_page, name='faq_page'),
]