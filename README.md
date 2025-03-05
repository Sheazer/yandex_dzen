
yandex_dzen/
│
├── Dockerfile                # Dockerfile для контейнеризации проекта
├── docker-compose.yml        # Docker Compose для управления сервисами
├── requirements.txt          # Список зависимостей проекта
├── manage.py                 # Основной файл Django
├── yandex_dzen/              # Директория с проектом Django
│   ├── __init__.py
│   ├── settings.py           # Настройки проекта
│   ├── urls.py               # URL маршруты
│   ├── wsgi.py               # WSGI-конфигурация
│   └── asgi.py               # ASGI-конфигурация
└── entrypoint.sh             # Скрипт для запуска проекта в Docker
```

## Требования

- Python 3.9+
- Docker и Docker Compose
- PostgreSQL (если используется для базы данных)

## Установка

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/Sheazer/yandex_dzen.git
cd yandex_dzen
```

### Шаг 2: Создайте `.env` файл

Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:

```dotenv
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

**Примечание**: Не забудьте заменить значения переменных на актуальные для вашего проекта.

### Шаг 3: Запустите Docker контейнеры

Для работы с Docker контейнерами выполните следующие шаги:

1. **Соберите образы**:

   ```bash
   docker-compose build
   ```

2. **Запустите контейнеры**:

   ```bash
   docker-compose up
   ```

3. После этого все контейнеры будут подняты, и ваше приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

## Использование

### Применение миграций

Для применения миграций в базе данных выполните команду:

```bash
docker-compose run web python manage.py migrate
```

### Создание суперпользователя

Для создания суперпользователя используйте команду:

```bash
docker-compose run web python manage.py createsuperuser
```

### Доступ к контейнерам

Для доступа к контейнеру с Django (например, для выполнения команд) используйте:

```bash
docker-compose exec web bash
```

### Просмотр логов

Чтобы просматривать логи приложения, используйте:

```bash
docker-compose logs -f
```

### Остановка контейнеров

Для остановки контейнеров выполните:

```bash
docker-compose down
```

## Контейнеризация с Docker

Проект контейнеризирован с использованием Docker. Вот как это работает:

- **Dockerfile**: файл для создания образа приложения. В нем устанавливаются все зависимости и конфигурируется запуск Django проекта.
- **docker-compose.yml**: конфигурационный файл для упрощения работы с несколькими контейнерами (например, веб-сервер и база данных).

### Dockerfile

Dockerfile для проекта:

```dockerfile
# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    netcat \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /yandex_dzen

# Копируем файл зависимостей в контейнер
COPY requirements.txt /yandex_dzen/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /yandex_dzen/

# Открываем порт 8000 для работы с приложением
EXPOSE 8000

# Указываем команду для запуска проекта
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.9'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: your_db_name
      POSTGRES_USER: your_db_user
      POSTGRES_PASSWORD: your_db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  web:
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/yandex_dzen
    ports:
      - 8000:8000
    depends_on:
      - db
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge
```

### entrypoint.sh

В `entrypoint.sh` мы добавляем команду для ожидания подключения базы данных перед запуском Django приложения:

```bash
#!/bin/sh

# Ожидаем подключения к базе данных
echo "Waiting for database to be ready..."
until nc -z -v -w30 db 5432; do
  echo "Waiting for database connection..."
  sleep 1
done

# Запускаем сервер
echo "Database connected. Starting Django server..."
exec "$@"
```

## Тестирование

1. Создайте посты через админку Django или API.
2. Убедитесь, что после публикации поста отправляется сообщение в Telegram.

### Примечания

- Убедитесь, что ваш **Telegram бот** имеет разрешение на отправку сообщений в чаты (пользователи должны быть подписаны на бота).
- Пример работы с PostgreSQL может потребовать настройки дополнительных параметров подключения в Django.

---

Теперь файл готов к использованию. Вы можете просто скопировать его в проект.