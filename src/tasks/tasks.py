from celery import Celery
from openpyxl import load_workbook

from src.core.config import app_config, load_rabbitmq_config
from src.tasks.db_updater import DataBaseUpdater
from src.tasks.excel_parser import ParseExcel

celery = Celery(
    'tasks',
    broker=load_rabbitmq_config().rabbitmq_url,
)


@celery.task(
    default_retry_delay=15,
)
def update_base():
    """Задача обновления данных в базе из файла."""
    parser = ParseExcel(load_workbook(app_config.excel_doc_path).worksheets[0])
    updater = DataBaseUpdater(parser.parse())
    updater.run()
