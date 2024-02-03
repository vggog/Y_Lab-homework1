import os

from dotenv import load_dotenv

from src.core.config.schemas import DBConfig, RedisConfig


load_dotenv()

db_config = DBConfig(
    db=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)


redis_config = RedisConfig(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    charset=os.getenv("REDIS_CHARSET"),
    decode_response=bool(int(os.getenv("REDIS_DECODE_RESPONSE"))),
)
