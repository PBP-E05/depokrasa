from django.urls import path
from .views import faq_page
from .views import show_json
from .views import post

app_name = 'feedback'

urlpatterns = [
    path('faq/', faq_page, name='faq_page'),
    path('json/', show_json, name='show_json'),
    path('post/', post, name='post'),
]