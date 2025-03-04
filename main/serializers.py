from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Rating, Post, Comment

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
        fields = ["id", "post", "user", "score"]
        read_only_fields = ["id", "user"]

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Это ваша модель пользователя (скорее всего, User или CustomUser)
        fields = ['username']


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "text", "author", "created_at", "average_rating"]
        read_only_fields = ["id", "text", "author", "created_at", "average_rating"]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
