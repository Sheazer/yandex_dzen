from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import User, Post, Comment


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'telegram_chat_id', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telegram_chat_id',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
