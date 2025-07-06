from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.timezone import now


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def specialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "likes": self.likes.count(),
            "liked": self.likes.filter(id=self.author.id).exists()
        }

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
