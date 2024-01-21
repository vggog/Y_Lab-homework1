from fastapi import Depends

from .repository import Repository


class Service:

    def __init__(
            self,
            repository=Depends(Repository),
    ):
        self.repository = repository

    def get_all_dishes(self):
        return self.repository.get_all()
