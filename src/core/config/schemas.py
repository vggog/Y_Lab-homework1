from dataclasses import dataclass


@dataclass
class DBConfig:
    db: str
    user: str
    password: str
    host: str
    port: str

    @property
    def alchemy_url(self) -> str:
        return (
            '{dialect_driver}'
            '://{username}:{password}@{host}:{port}/{database}'
        ).format(
            dialect_driver='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )


@dataclass
class RabbitMQConfig:
    user: str
    password: str
    port: str
    host: str

    @property
    def rabbitmq_url(self) -> str:
        return 'amqp://{user}:{password}@{host}:{port}'.format(
            user=self.user,
            password=self.password,
            port=self.port,
            host=self.host,
        )


@dataclass
class RedisConfig:
    host: str
    port: int
    charset: str
    decode_response: bool


@dataclass
class AppConfig:
    excel_doc_path: str
    url_prefix = 'http://back:8000/api/v1'
    menus_postfix = '/menus'
    submenus_postfix = '/menus/{menu_id}/submenus'
    dishes_postfix = '/menus/{menu_id}/submenus/{submenu_id}/dishes'
