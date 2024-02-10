import os

from dotenv import load_dotenv

from src.core.config.schemas import DBConfig, RedisConfig, RabbitMQConfig


load_dotenv()


def load_db_config() -> DBConfig:
    """Функция для проверки наличия атрибутов и их загрузки"""
    db = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')

    if (not db) or (not user) or (not password) or (not host) or (not port):
        raise TypeError('Конфиги не заполнены.')

    return DBConfig(
        db=db,
        user=user,
        password=password,
        host=host,
        port=port,
    )


def load_redis_config() -> RedisConfig:
    """Функция для проверки наличия атрибутов и их загрузки"""
    host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_response = os.getenv('REDIS_DECODE_RESPONSE')
    charset = os.getenv('REDIS_CHARSET')

    if (not host) or (not redis_port) or (not redis_response) or (not charset):
        raise TypeError('Конфиги не заполнены.')

    return RedisConfig(
        host=host,
        port=int(redis_port),
        charset=charset,
        decode_response=bool(int(redis_response)),
    )


def load_rabbitmq_config() -> RabbitMQConfig:
    """Функция для проверки и загрузки конфигов для RabbitMQ"""
    user = os.getenv('RABBITMQ_DEFAULT_USER')
    password = os.getenv('RABBITMQ_DEFAULT_PASS')
    port = os.getenv('RABBITMQ_DEFAULT_PORT')
    host = os.getenv('RABBITMQ_HOST')

    if (not user) or (not password) or (not port) or (not host):
        raise TypeError('Конфиги RabbitMQне заполнены.')

    return RabbitMQConfig(
        user=user,
        password=password,
        port=port,
        host=host
    )


db_config = load_db_config()
redis_config = load_redis_config()
