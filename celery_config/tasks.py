import os
import random
from celery import Celery
from dotenv import load_dotenv
from SMTP.email import send_email

load_dotenv()

celery_app = Celery('celery_app', broker='redis://localhost:6379')

my_mail = os.environ.get('EMAIL')
smtp_login = os.environ.get('smtp_login')
smtp_password = os.environ.get('smtp_password')


@celery_app.task
def send_mail_with_pass(email: str):
    password = random.randint(100000, 999999)
    send_email(
        mail_from=my_mail,
        mail_to=email,
        user_pass=password,
        smtp_login=smtp_login,
        smtp_password=smtp_password
    )
