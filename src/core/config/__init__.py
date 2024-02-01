import os

from dotenv import load_dotenv

from .schemas import DBConfig


load_dotenv()

db_config = DBConfig(
    db=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
