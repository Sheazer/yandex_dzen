from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsStaffOrReadOnly(BasePermission):
    """
    Пользователи с is_staff=True могут редактировать и удалять объекты.
    Остальные могут только читать.
    """

    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Для остальных методов проверяем, что пользователь авторизован и is_staff=True
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Для остальных методов проверяем, что пользователь авторизован и is_staff=True
        return request.user.is_authenticated and request.user.is_staff


class ListCrudView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """
    Универсальный класс для обработки всех CRUD операций:
    - GET (список и детали объекта)
    - POST (создание объекта)
    - PUT/PATCH (обновление объекта, только для is_staff)
    - DELETE (удаление объекта, только для is_staff)
    """
    queryset = None  # Queryset должен быть переопределен в дочернем классе
    serializer_class = None  # Сериализатор должен быть переопределен в дочернем классе
    lookup_field = 'pk'  # Поле для поиска объекта (по умолчанию 'pk')
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]  # Права доступа

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запросы:
        - Если передан lookup_field (например, pk), возвращает детали объекта.
        - Иначе возвращает список объектов.
        """
        if kwargs.get(self.lookup_field):
            # Детализация объекта
            return self.retrieve(request, *args, **kwargs)
        else:
            # Список объектов
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запросы для создания нового объекта.
        """
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Обрабатывает PUT-запросы для полного обновления объекта.
        Только для пользователей с is_staff=True.
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Обрабатывает PATCH-запросы для частичного обновления объекта.
        Только для пользователей с is_staff=True.
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Обрабатывает DELETE-запросы для удаления объекта.
        Только для пользователей с is_staff=True.
        """
        return self.destroy(request, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Обрабатывает исключения и возвращает соответствующий HTTP-ответ.
        """
        if isinstance(exc, Exception):
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)
