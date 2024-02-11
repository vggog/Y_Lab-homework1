from src.factory import AppFactory
from src.tasks.tasks import update_base

app = AppFactory.create_app()


@app.on_event('startup')
def start_up_project():
    update_base.delay()
