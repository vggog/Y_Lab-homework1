from celery import Celery

from src.core.config import load_rabbitmq_config

celery = Celery(
    'tasks',
    broker=load_rabbitmq_config().rabbitmq_url,
)


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_base():
    """Задача обновления данных в базе из файла."""
    print('work')
