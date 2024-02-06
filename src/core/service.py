class BaseService:

    @staticmethod
    def delete_non_value_key(data: dict[str, str | None]) -> dict[str, str]:
        """Метод для удаления ключей со значениями None"""
        updated_dict: dict[str, str] = {
            k: v for k, v in data.items() if v is not None
        }

        return updated_dict
