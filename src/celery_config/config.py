from celery import Celery

from src.config import settings

redis_link = f'redis://{settings.REDIS_USER}:{settings.REDIS_PASS}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'

celery_app = Celery('celery_app', broker=redis_link)
celery_app.conf.task_always_eager = False
