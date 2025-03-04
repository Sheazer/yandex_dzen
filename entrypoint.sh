#!/bin/sh

echo "Ожидание PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL доступен!"

# Выполняем миграции
python manage.py migrate
python manage.py collectstatic --noinput

# Запускаем сервер
exec "$@"
