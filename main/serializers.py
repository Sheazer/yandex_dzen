from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Rating, Post

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'telegram_chat_id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            telegram_chat_id=validated_data['telegram_chat_id'],
        )
        return user


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score', 'post']


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'published_at', 'author', 'average_rating', 'ratings']

    def create(self, validated_data):
        # Создание поста
        post = Post.objects.create(**validated_data)
        post.update_average_rating()
        return post

    def update(self, instance, validated_data):
        # Обновление поста
        instance = super().update(instance, validated_data)
        instance.update_average_rating()
        return instance
