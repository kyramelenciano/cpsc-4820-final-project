from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .email_receipts import fetch_gmail_receipts
from django.conf import settings

# disable googleapiclient logs
import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class ReceiptsProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receipts_processing'

    def ready(self) -> None:
        if settings.GMAIL_SYNC_ENABLED:
            scheduler = BackgroundScheduler()
            job = scheduler.add_job(
                fetch_gmail_receipts, 'interval', minutes=1)
            scheduler.start()
