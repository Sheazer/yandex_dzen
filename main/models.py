from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    text = models.TextField(max_length=250, verbose_name="Text")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added time")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User", verbose_name="Author")

    def __str__(self):
        return self.text[:50]

    def get_average_rating(self):
        return self.ratings.aggregate(avg=Avg("score"))["avg"] or 0


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f'{self.post.author} - {self.score}'


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  
    author_name = models.CharField(max_length=255, blank=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post
