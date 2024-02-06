from fastapi import FastAPI
from starlette.datastructures import URLPath


def reverse(app: FastAPI, name: str, **kwargs) -> URLPath:
    return app.url_path_for(name, **kwargs)
