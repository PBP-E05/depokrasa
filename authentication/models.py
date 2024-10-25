from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.jpg', blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username