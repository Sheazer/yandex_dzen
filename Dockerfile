# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /yandex_dzen

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Ожидание PostgreSQL перед стартом
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /yandex_dzen/entrypoint.sh

# Для не Windows
#ENTRYPOINT ["/yandex_dzen/entrypoint.sh"]

# Для windows
ENTRYPOINT ["bash", "/yandex_dzen/entrypoint.sh"]

