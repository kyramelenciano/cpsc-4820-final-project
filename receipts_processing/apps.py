from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .email_receipts import fetch_gmail_receipts

# disable googleapiclient logs
import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class ReceiptsProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receipts_processing'

    def ready(self) -> None:
        scheduler = BackgroundScheduler()
        job = scheduler.add_job(fetch_gmail_receipts, 'interval', minutes=1)
        scheduler.start()
