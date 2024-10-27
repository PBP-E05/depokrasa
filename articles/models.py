from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "categories"

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField('Title',max_length=255)
    featured_img = models.ImageField(upload_to="article_featured_image/", blank=True, null=True)
    body = CKEditor5Field('Text', config_name='default')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'featured_img': self.featured_img.url if self.featured_img else None,
            'body': self.body,
            'created_on': self.created_on.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'categories': [category.name for category in self.categories.all()] 
        }

    def __str__(self):
        return self.title    
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.article.title}"
    
    def get_author_data(self):
        return {
            'username': self.author.username,
            'profile_picture': self.author.userprofile.profile_picture.url if hasattr(self.author, 'userprofile') and self.author.userprofile.profile_picture else '/media/profile_pictures/default.jpg'
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'created_on': self.created_on.isoformat(),
            'author': self.get_author_data(),
            'article_id': self.article_id
        }