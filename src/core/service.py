class BaseService:

    @staticmethod
    def delete_non_value_key(data: dict) -> dict:
        """Метод для удаления ключей со значениями None"""
        updated_dict = {
            k: v for k, v in data.items() if v is not None
        }

        return updated_dict
