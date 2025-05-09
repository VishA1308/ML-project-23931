# A Dockerfile is a text document that contains all the commands
# a user could call on the command line to assemble an image.

FROM python:3.11-buster

# Обновление списка пакетов
RUN apt update

# Установка необходимых библиотек
RUN apt install -y libgl1-mesa-glx
RUN apt-get -y install tesseract-ocr tesseract-ocr-rus

# Создание папки для сборки
RUN mkdir build

# Установка рабочей директории
WORKDIR /build

# Копирование файлов в контейнер
COPY . .

# Обновление pip и установка зависимостей
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Загрузка необходимых ресурсов NLTK
RUN python3 -c "import nltk; nltk.download('stopwords')"
RUN python3 -c "import nltk; nltk.download('punkt')"
RUN python3 -c "import nltk; nltk.download('punkt_tab')"
RUN python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
RUN cp -r /root/nltk_data /usr/local/share/nltk_data 

# Открытие порта 8080
EXPOSE 8080

# Установка рабочей директории для приложения
WORKDIR /build/app

# Запуск сервера uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
