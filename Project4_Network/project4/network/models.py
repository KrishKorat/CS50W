from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.timezone import now


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author} posted on {self.timestamp}"
    
