import requests as requests
import uuid # для генерации случайных имен файлов
import time
from django.conf import settings
from celery import shared_task
from random import randint


# Create your tasks here

CAT_URL = 'http://thecatapi.com/api/images/get?format=src&type=gif'


@shared_task
def download_a_cat():
    resp = requests.get(CAT_URL)
    # получаем расширение файла
    file_ext = resp.headers.get('Content-Type').split('/')[1]
    # создаем имя файла
    # = имя базовой директории / cats / рандомное имя . расширение
    file_name = settings.BASE_DIR / 'cats' / (str(uuid.uuid4()) + "." + file_ext)

    # открываем файл на запись в режиме байтов wb
    with open(file_name, 'wb') as f:
        # и записываем каждый chunk
        # из resp.iter_content
        # в файл f
        for chunk in resp.iter_content(chunk_size=128):
            f.write(chunk)

    return True


@shared_task
def cpu_task():
    time_to_sleep = randint(5, 70)
    time.sleep(time_to_sleep)
    return f"I slept for {time_to_sleep} secs"

