import asyncio
import os
import random
from celery import Celery
from dotenv import load_dotenv
from pydantic import EmailStr

from SMTP.email_functions import send_password_mail, send_accept_mail

load_dotenv()

celery_app = Celery('celery_app', broker='redis://localhost:6379')
celery_app.conf.task_always_eager = False

smtp_login = os.environ.get('smtp_login')
smtp_password = os.environ.get('smtp_password')


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
