from celery import Celery

celery_app = Celery()


@celery_app.task
def send_mail_with_pass(email: str):
    create_pass = 'pass'
    send_mail = 'pass'
