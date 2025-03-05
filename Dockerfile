# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /yandex_dzen

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Указываем команду для запуска
CMD ["gunicorn", "yandex_dzen.wsgi:application", "--bind", "0.0.0.0:8000"]