import asyncio
import random
from pydantic import EmailStr

from src.celery_config.config import celery_app
from src.smtp_config.smtp_tasks import send_password_mail, send_accept_mail


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
