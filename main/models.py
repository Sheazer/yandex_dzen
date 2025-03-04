from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class User(BaseUserManager):
    def create_user(self, username, telegram_chat_id, email, password=None):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(username=username, telegram_chat_id=telegram_chat_id, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

