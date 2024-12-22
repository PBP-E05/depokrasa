from django.urls import path
from articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', show_articles, name='show_articles'),
    path('<int:pk>/', article_content, name='article_content'),
    path('category/<category>/', show_article_category, name='show_article_category'),
    path('get-articles-by-category/<category>/', show_articles_by_category_json, name='show_articles_by_category_json'),
    path('get-articles/', show_articles_json, name='show_articles_json'),
    path('get-categories/', show_categories_json, name='show_categories_json'),
    path('get-article/<int:pk>/', show_article_by_id_json, name='show_article_by_id'),
    path('get-comments/<int:pk>/', show_comments_json, name='show_comments_json'),
    path('add-comment/', add_comment_ajax, name='add_comment_ajax')
]