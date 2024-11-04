import aiosmtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import NoReturn

import aiosmtplib
from loguru import logger
from pydantic import EmailStr

from config import settings
from src.redis_config.crud import put_session
from src.redis_config.schemas import RedisLoginData

smtp_login = settings.SMTP_LOGIN
smtp_password = settings.SMTP_PASSWORD


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
            hostname='smtp_config.yandex.ru',
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
            hostname='smtp_config.yandex.ru',
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
