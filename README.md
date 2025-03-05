# Yandex Dzen - Django + Docker + PostgreSQL + Telegram Bot

## Описание

Yandex Dzen — это веб-приложение, созданное на Django, с возможностью публикации постов и отправки уведомлений в Telegram.

В проекте используются:
- **Django** – фреймворк для веб-приложений
- **PostgreSQL** – база данных
- **Docker и Docker Compose** – контейнеризация
- **Postman** – тестирование API
- **Telegram Bot** – для отправки уведомлений пользователям

---

## 1. Установка и настройка

### 1.1. Клонируем репозиторий
```bash
git clone https://github.com/your-repository-url.git
cd yandex_dzen
```

### 1.2. Создаём виртуальное окружение (локальный запуск без Docker, опционально)
Если планируете запускать без Docker:
```bash
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

### 1.3. Создаём `.env` файл
Создайте файл `.env` в корне проекта:
```dotenv
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=yandex_dzen
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- **TELEGRAM_BOT_TOKEN** – получите у [@BotFather](https://t.me/BotFather).
- **DB_HOST=db** – указывает на сервис базы данных в Docker.

---

## 2. Запуск проекта в Docker

### 2.1. Собираем контейнеры
```bash
docker-compose build
```

### 2.2. Запускаем проект
```bash
docker-compose up -d
```

После этого приложение будет доступно по адресу:
[http://localhost:8000](http://localhost:8000)

---

## 3. Работа с базой данных

### 3.1. Применяем миграции
```bash
docker-compose run web python manage.py migrate
```

### 3.2. Создаём суперпользователя
```bash
docker-compose run web python manage.py createsuperuser
```
Теперь можно зайти в админ-панель:
[http://localhost:8000/admin](http://localhost:8000/admin)

---

## 4. Работа с API через Postman

1. **Открываем Postman**
2. **Импортируем файл yandex.postman_collection.json**
3. **Выбираем метод `POST` и указываем URL:**
   ```
   http://localhost:8000/api/login/
   ```
4. **В Body (JSON) передаем данные:**
   ```json
   {
      "username": "user",
      "password": "pass"
   }
   ```
5. **Нажимаем `Send`**

### 4.1. Проверка ответа API
```json
{
   "refresh": "refresh_token",
   "access": "token",
}
```
Везде в заголовке запросов нужно использовать access_token.
Выбирайте Bearer token.

### 4.2. Уведомление в Telegram
Если у пользователя есть `telegram_chat_id`, бот отправит сообщение в Telegram. 
При создании постов.
---

## 5. Файлы проекта и их назначение

### 5.1. `Dockerfile`
```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat && apt-get clean

WORKDIR /yandex_dzen

COPY requirements.txt /yandex_dzen/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /yandex_dzen/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 5.2. `docker-compose.yml`
```yaml
version: '3.9'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: yandex_dzen
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
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
      - "8000:8000"
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

### 5.3. `entrypoint.sh`
```bash
#!/bin/sh

until nc -z -v -w30 db 5432; do
  echo "Ожидание..."
  sleep 1
done

exec "$@"
```

---

## 6. Частые ошибки и их исправление

### 6.1. `zsh: command not found: docker-compose`
```bash
docker-compose --version
```
Если нет, установите:
```bash
sudo apt install docker-compose
```

### 6.2. `ERROR: No matching distribution found for -r requirements.txt`
```bash
ls -l requirements.txt
```

### 6.3. `Database connection refused`
```bash
docker-compose ps
docker-compose down && docker-compose up -d
```

---

## 7. Остановка контейнеров
```bash
docker-compose down
```

---

## 8. Разработка и тестирование
Редактируйте файлы в редакторе, Docker автоматически применит изменения после перезапуска.

---
