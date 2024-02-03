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
        data_for_saving = schema(**data.__dict__)

        self._redis_client().set(key, value=data_for_saving.model_dump_json())

    def get_value(self, key: str):
        data = self._redis_client().get(name=key)
        if data is None:
            return None

        return json.loads(data)

    def delete_value(self, key: str) -> None:
        self._redis_client().delete(key)
