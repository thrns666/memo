redis server
celery -A celery_config.tasks:celery_app worker --loglevel=INFO --pool=solo
