from fastapi import FastAPI

from .menu.views import menus_router


class AppFactory:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI(
            root_path="/api/v1"
        )
        cls._append_routes(app)
        return app

    @staticmethod
    def _append_routes(app: FastAPI):
        app.include_router(menus_router)
