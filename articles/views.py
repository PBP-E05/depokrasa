from articles.models import Article, Comment
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_articles(request):
    articles = Article.objects.all().order_by("-created_on")
    context = {
        "articles": articles,
    }

    return render(request, "index.html", context)


def show_article_category(request, category):
    articles = Article.objects.filter(categories__name__contains = category).order_by("-created_on")
    context = {
        "category": category,
        "articles": articles,
    }

    return render(request, "category.html", context)

def article_content(request, pk):
    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article).order_by("-created_on")
    context = {
        "article": article,
        "comments": comments,
    }

    return render(request, "content.html", context)

def show_articles_json(request):
    articles = Article.objects.all().order_by("-created_on")
    data = [article.to_dict() for article in articles]
    return JsonResponse(data, safe=False)

def show_articles_by_category_json(request, category):
    articles = Article.objects.filter(categories__name__contains= category).order_by("-created_on")
    data = [article.to_dict() for article in articles]
    return JsonResponse(data, safe=False)

def show_comments_json(request):
    article_id = request.GET.get('article_id')
    if not article_id:
        return JsonResponse([], safe=False)
    
    comments = Comment.objects.filter(article_id=article_id).select_related('author').order_by("-created_on")
    comments_data = [comment.to_dict() for comment in comments]
    
    return JsonResponse(comments_data, safe=False)

@csrf_exempt
@require_POST
def add_comment_ajax(request):
    comment_body = request.POST.get("comment")
    user =request.user
    article_id=request.POST.get("article_id")
    article = get_object_or_404(Article, id=article_id)

    if comment_body and user.is_authenticated:
        new_comment = Comment(
            body=comment_body,
            author=user,
            article=article
        )
        new_comment.save()
        return JsonResponse(new_comment.to_dict(), status=201)
    else:
        return JsonResponse({"error":"BAD REQUEST: empty comment"}, status=400)

