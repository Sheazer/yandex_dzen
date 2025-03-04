# Используем базовый образ, например, ubuntu
FROM ubuntu:20.04

# Устанавливаем netcat и другие нужные пакеты
RUN apt-get update && apt-get install -y netcat

# Копируем ваш код и выполняем другие действия
# Например, копирование файлов приложения:
COPY . /yandex_dzen/

# Устанавливаем рабочую директорию
WORKDIR /yandex_dzen

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем entrypoint
ENTRYPOINT ["/yandex_dzen/entrypoint.sh"]
