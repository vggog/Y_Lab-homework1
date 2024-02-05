from fastapi import FastAPI


def reverse(app: FastAPI, name: str, **kwargs):
    return app.url_path_for(name, **kwargs)
