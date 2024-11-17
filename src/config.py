import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: str = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASS: str = os.environ.get('DB_PASS')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_HOST_TEST: str = os.environ.get('DB_HOST_TEST')
    DB_PORT_TEST: str = os.environ.get('DB_PORT_TEST')
    DB_USER_TEST: str = os.environ.get('DB_USER_TEST')
    DB_PASS_TEST: str = os.environ.get('DB_PASS_TEST')
    DB_NAME_TEST: str = os.environ.get('DB_NAME_TEST')

    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')
    REDIS_USER: str = os.environ.get('REDIS_USER')
    REDIS_PASS: str = os.environ.get('REDIS_PASS')

    SMTP_LOGIN: str = os.environ.get('SMTP_LOGIN')
    SMTP_PASSWORD: str = os.environ.get('SMTP_PASSWORD')

    GIGA_CHAT_CLIENT_ID: str = os.environ.get('GIGA_CHAT_CLIENT_ID')
    GIGA_CHAT_CLIENT_SECRET: str = os.environ.get('GIGA_CHAT_CLIENT_SECRET')


settings = Settings()
