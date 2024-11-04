import asyncio

import random
from celery import Celery
from pydantic import EmailStr

from src.smtp_config.smtp_tasks import send_password_mail, send_accept_mail
from config import settings

celery_app = Celery('celery_app', broker=f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')
celery_app.conf.task_always_eager = False


@celery_app.task
def send_mail_with_pass(email: EmailStr):
    password = random.randint(100000, 999999)
    try:
        asyncio.run(
            send_password_mail(
                mail_to=email,
                user_pass=password,
            )
        )
        return True
    except Exception as ex:
        return ex


@celery_app.task
def send_acceptance_mail(email: EmailStr):
    try:
        asyncio.run(
            send_accept_mail(
                mail_to=email
            )
        )
        return True
    except Exception as ex:
        return ex
