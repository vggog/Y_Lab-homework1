import os

from dotenv import load_dotenv

from src.core.config.schemas import DBConfig, RedisConfig


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


redis_config = load_redis_config()
