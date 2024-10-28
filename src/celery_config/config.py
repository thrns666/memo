import os

from dotenv import load_dotenv

load_dotenv()

smtp_login = os.environ.get('smtp_login')
smtp_password = os.environ.get('smtp_password')
