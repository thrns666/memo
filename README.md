____
# Memo
## Memo — ***это приложение для создания и хранения заметок.***

## Stack

FastAPI
Redis
Celery
Alembic 
SQLAlchemy
SMTP
JWT
Asyncpg

## Структура проекта

- src/ — исходный код приложения.
- alembic/ — управление миграциями базы данных.
- static/ — статические файлы.
- tests/ — тесты для проверки функциональности.

## Установка

### Клонируйте репозиторий:

- git clone https://github.com/thrns666/memo
- cd memo-dev

- pip install -r requirements.txt

### Запуск локально:

- redis-server
- celery -A celery_config.tasks:celery_app worker --loglevel=INFO --pool=solo
- python src/main.py
_____
