# Установка необходимых зависимостей
FROM ubuntu:latest


RUN apt-get update && apt-get install -y xvfb


# Установка Python и других необходимых зависимостей
RUN apt-get install -y python3 python3-pip

RUN pip3 install requests pandas plotly numpy plotly beautifulsoup4 tensorflow scikit-learn

# Создание рабочей директории в контейнере
WORKDIR /app

# Копирование файлов в рабочую директорию
COPY . /app

# Установка Xvfb и настройка переменной окружения DISPLAY
ENV DISPLAY=:99
CMD Xvfb :99 -screen 0 1024x768x16 & python3 RUN.py