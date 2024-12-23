from django.urls import path
from .views import faq_page
from .views import show_json
from .views import edit_feedback
from .views import delete_feedback
from .views import submit_feedback_anonymous

app_name = 'feedback'

urlpatterns = [
    path('faq/', faq_page, name='faq_page'),
    path('json/', show_json, name='show_json'),
    path('edit/<int:feedback_id>/', edit_feedback, name='edit_feedback'),
    path('delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('submit_feedback_anonymous/', submit_feedback_anonymous, name='submit_feedback_anonymous'),
]