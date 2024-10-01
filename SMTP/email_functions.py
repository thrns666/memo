import asyncio
import os
import aiosmtplib
import traceback
from typing import NoReturn
from dotenv import load_dotenv
from loguru import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from redis_config.models import RedisLoginData
from redis_config.redis_crud import put_session

load_dotenv()

smtp_login = os.environ.get('SMTP_LOGIN')
smtp_password = os.environ.get('SMTP_PASSWORD')
to_mail = user_password = ''
letter = f'''
From: {smtp_login}
To: {to_mail}
Subject: Memo Notes service
Content-Type: text/plain

Your password for auth in Memo Notes: {user_password}
'''
body = '000000'


async def send_email(mail_to: str, user_pass: int) -> NoReturn | None:
    try:
        data = RedisLoginData(email=mail_to, user_password=user_pass)
        await put_session(data)
        msg = MIMEMultipart()
        msg['From'] = smtp_login
        msg['To'] = mail_to
        msg['Subject'] = 'Password Memo Notes'
        msg.attach(MIMEText(f'{user_pass}', 'plain'))
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
        logger.error(f'Error in send_mail: {ex} -- {tb}')
        return None
