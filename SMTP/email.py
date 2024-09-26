import smtplib
from typing import NoReturn
from loguru import logger

from redis_config.redis_crud import put_session

my_mail = to_mail = user_password = ''
letter = f'''
From: {my_mail}
To: {to_mail}
Subject: Memo Notes service
Content-Type: text/plain

Your password for auth in Memo Notes: {user_password}
'''


def send_email(mail_from: str, mail_to: str, user_pass: int, smtp_login: str, smtp_password: str) -> NoReturn | None:
    letter_message = letter.format(my_mail=mail_from, to_mail=mail_to, user_password=user_pass).encode('UTF-8')
    server = smtplib.SMTP_SSL('smtp.gmail.com:587')
    try:
        put_session({'email': mail_to, 'user_password': user_pass})
        server.login(smtp_login, smtp_password)
        server.sendmail(mail_from, mail_to, letter_message)
    except Exception as ex:
        logger.error(f'Error in send_mail: {ex}')
        return None
    finally:
        server.quit()
