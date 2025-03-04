from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from telegram import TelegramError

from main.models import Post
from main.serializers import PostSerializer
from tg_bot.utils import send_telegram_message


class IsStaffOrReadOnly(BasePermission):
    """
    Пользователи с is_staff=True могут редактировать и удалять объекты.
    Остальные могут только читать.
    """

    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        # Для остальных методов проверяем, что пользователь авторизован и is_staff=True
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True

        return request.user.is_authenticated and (request.user == obj.author or request.user.is_staff)


class ListCrudView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                post = Post.objects.get(id=pk)
                serializer = self.serializer_class(post)
                return Response(serializer.data)
            except Post.DoesNotExist:
                raise NotFound({"detail": "Post not found"})
        else:
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data)

    def post(self, request):
        data = request.data
        text = data.get('text')
        if not text:
            return Response({"detail": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(text=text, author=request.user)
        serializer = self.serializer_class(post)

        telegram_chat_id = request.user.telegram_chat_id

        if telegram_chat_id:
            try:
                send_telegram_message(chat_id=telegram_chat_id)
            except TelegramError as e:
                print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise NotFound({"detail": "Post not found"})

        if request.user != post.author and not request.user.is_staff:
            return Response({"detail": "You do not have permission to update this post"},
                            status=status.HTTP_403_FORBIDDEN)

        post.text = request.data.get("text", post.text)
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise NotFound({"detail": "Post not found"})

        if request.user != post.author and not request.user.is_staff:
            return Response({"detail": "You do not have permission to update this post"},
                            status=status.HTTP_403_FORBIDDEN)

        post.text = request.data.get("text", post.text)
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise NotFound({"detail": "Post not found"})

        if request.user != post.author and not request.user.is_staff:
            return Response({"detail": "You do not have permission to delete this post"},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"detail": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
