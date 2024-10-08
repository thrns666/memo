import os
import aiosmtplib
import traceback
from typing import NoReturn
from dotenv import load_dotenv
from loguru import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pydantic import EmailStr

from redis_config.models import RedisLoginData
from redis_config.redis_crud import put_session

load_dotenv()

smtp_login = os.environ.get('SMTP_LOGIN')
smtp_password = os.environ.get('SMTP_PASSWORD')


async def send_password_mail(mail_to: EmailStr, user_pass: int) -> NoReturn | None:
    data = RedisLoginData(email=mail_to, user_password=user_pass)
    msg = MIMEMultipart()
    msg['From'] = smtp_login
    msg['To'] = mail_to
    msg['Subject'] = 'Password Memo Notes'
    msg.attach(MIMEText(f'{user_pass}', 'plain'))

    try:
        await put_session(data)
        await aiosmtplib.send(
            msg,
            hostname='smtp.yandex.ru',
            port=587,
            username=smtp_login,
            password=smtp_password,
            start_tls=True
        )
        logger.info(f'Send mail to - {mail_to}')
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in send_password_mail: {ex} -- {tb}')
        return None


async def send_accept_mail(mail_to: EmailStr) -> NoReturn | None:
    msg = MIMEMultipart()
    msg['From'] = smtp_login
    msg['To'] = mail_to
    msg['Subject'] = 'Memo Notes'
    msg.attach(MIMEText(f'Welcome and thanks for Your registration on Memo Notes', 'plain'))

    try:
        await aiosmtplib.send(
            msg,
            hostname='smtp.yandex.ru',
            port=587,
            username=smtp_login,
            password=smtp_password,
            start_tls=True
        )
        logger.info(f'Send mail to - {mail_to}')
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in send_accept_mail: {ex} -- {tb}')
        return None
