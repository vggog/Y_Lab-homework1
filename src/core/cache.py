import json
from typing import Any

import redis.asyncio as redis

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

    async def set_value(self, key: str, data: BaseModel, schema) -> None:
        """
        Метод для сохранения данных в redis
        key: ключ,
        data: данные, которые сохраняются,
        schema: pydantic-схема, с помощью которого данные преобразуются в json
            и сохраняются в redis.
        """
        data_for_saving = schema(**data.__dict__)
        await self._redis_client().set(
            key,
            value=data_for_saving.model_dump_json()
        )

    async def set_list_of_values(
            self,
            key: str,
            datas: list[BaseModel],
            schema
    ) -> None:
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

        await self._redis_client().set(key, value=json.dumps(saving_datas))

    async def get_value(
            self,
            key: str
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """Метод для получения данных."""
        data = await self._redis_client().get(name=key)
        if data is None:
            return None

        return json.loads(data)

    async def delete_value(self, key: str) -> None:
        """Удалить значение"""
        await self._redis_client().delete(key)

    async def get_discounts(self) -> dict[str, int]:
        """Получить словарь со скидками"""
        discounts: dict[str, int] = json.loads(
            await self._redis_client().get(name='discounts')
        )
        if discounts is None:
            return {}

        return discounts

    async def get_discount_of_dish(self, dish_id: str) -> int:
        """
        Получить скидку определённого блюда.
        Если информации о скидки нет, то вернёт 0.
        """
        discounts: dict[str, int] = await self.get_discounts()
        try:
            return discounts[dish_id]
        except KeyError:
            return 0

    async def set_discounts(self, discounts: dict[str, int]) -> None:
        """Сохранить информацию о скидках."""
        await self._redis_client().set(
            'discounts',
            value=json.dumps(discounts)
        )

    async def append_discounts(self, dish_id: str, disc: int) -> None:
        """Добавить запись о скидке для определённого продукта."""
        discounts: dict[str, int] = await self.get_discounts()
        discounts[dish_id] = disc
        await self.set_discounts(discounts)
