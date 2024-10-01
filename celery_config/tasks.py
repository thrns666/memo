import asyncio
import os
import random
from celery import Celery
from dotenv import load_dotenv
from SMTP.email_functions import send_email

load_dotenv()

celery_app = Celery('celery_app', broker='redis://localhost:6379')
celery_app.conf.task_always_eager = False

smtp_login = os.environ.get('smtp_login')
smtp_password = os.environ.get('smtp_password')


@celery_app.task
def send_mail_with_pass(email: str):
    password = random.randint(100000, 999999)
    asyncio.run(
        send_email(
            mail_to=email,
            user_pass=password,
        )
    )
    return True
