from django.db.models import Avg
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import asyncio

from telegram.error import TelegramError

from main.serializers import UserRegistrationSerializer, PostSerializer, RatingSerializer, CommentSerializer, \
    UserSerializer, CommentEditSerializer
from main.BaseView import ListCrudView
from main.models import Post, Rating, Comment, User
from tg_bot.utils import send_telegram_message


class CustomTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountView(ListAPIView):
    queryset = User.objects.all()  # Получаем всех пользователей
    serializer_class = UserSerializer  # Сериализатор для пользователей


class PostView(ListCrudView):
    queryset = Post.objects.annotate(average_rating=Avg("ratings__score"))
    serializer_class = PostSerializer
    lookup_field = 'pk'




class CommentEditView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentEditSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        # Фильтруем комментарии по конкретному посту
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_update(self, serializer):
        # Получаем текущий комментарий
        comment = self.get_object()

        # Проверяем, имеет ли пользователь право редактировать этот комментарий
        if comment.author_name != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this comment.")

        # Извлекаем только текст из запроса, оставляем все остальные поля без изменений
        text = self.request.data.get('text')

        if text:
            # Обновляем только текст комментария, оставляя авторов и пост неизменными
            comment.text = text
            comment.save()

        # Возвращаем обновленный комментарий
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        # Удаление только для is_staff или владельца комментария
        if instance.author_name != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()


class CommentListCreateView(APIView):
    """
    Обрабатывает создание и получение комментариев для поста.
    - GET: Получение всех комментариев для указанного поста.
    - POST: Добавление нового комментария к посту.
    """

    def get(self, request, post_id, *args, **kwargs):
        """
        Получение списка всех комментариев для указанного поста.
        """
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id, *args, **kwargs):
        """
        Добавление нового комментария к указанному посту.
        """
        data = request.data.copy()  # Делаем копию, чтобы изменять

        data['post'] = post_id  # Привязываем комментарий к посту

        # Если пользователь авторизован, используем его username
        if request.user.is_authenticated:
            data['author_name'] = request.user.username
        else:
            # Если пользователь не указал username, используем "Anonymous"
            data['author_name'] = data.get('author_name', 'Anonymous')

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Сохраняем новый комментарий
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Пост не найден"}, status=status.HTTP_404_NOT_FOUND)

        score = int(request.data.get('score'))
        if score is None or not (1 <= score <= 5):
            return Response({"error": "Оценка должна быть от 1 до 5"}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={"score": score}
        )

        # Возвращаем результат
        return Response(RatingSerializer(rating).data,
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
