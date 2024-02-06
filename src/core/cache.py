import json

import redis

from src.core.config import redis_config
from src.core.model import BaseModel


class Cache:
    redis_conf = redis_config

    def _redis_client(self):
        return redis.StrictRedis(
            host=self.redis_conf.host,
            port=self.redis_conf.port,
            encoding=self.redis_conf.charset,
            decode_responses=self.redis_conf.decode_response,
        )

    def set_value(self, key: str, data: BaseModel, schema) -> None:
        """
        Метод для сохранения данных в redis
        key: ключ,
        data: данные, которые сохраняются,
        schema: pydantic-схема, с помощью которого данные преобразуются в json
            и сохраняются в redis.
        """
        data_for_saving = schema(**data.__dict__)
        self._redis_client().set(key, value=data_for_saving.model_dump_json())

    def set_list_of_values(self, key: str, datas: list[BaseModel], schema) -> None:
        """
        Метод для сохранения списка данных.
        :param key: ключ
        :param datas: список данных
        :param schema: pydantic-схема, с помощью которого каждый элемент списка
                        преобразуются в json.
        :return:
        """
        saving_datas = []
        for data in datas:
            saving_datas.append(schema(**data.__dict__).model_dump())

        self._redis_client().set(key, value=json.dumps(saving_datas))

    def get_value(
            self,
            key: str
    ) -> list[dict[str, str]] | dict[str, str] | None:
        """Метод для получения данных."""
        data = self._redis_client().get(name=key)
        if data is None:
            return None

        return json.loads(data)

    def delete_value(self, key: str) -> None:
        self._redis_client().delete(key)
