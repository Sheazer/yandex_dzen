from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(unique=True, null=True, blank=True)


