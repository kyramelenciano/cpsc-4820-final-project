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

    # doc: https://docs.djangoproject.com/en/4.1/ref/applications/#django.apps.AppConfig.ready
    def ready(self) -> None:
        if settings.GMAIL_SYNC_ENABLED:
            # doc: https://apscheduler.readthedocs.io/en/3.x/userguide.html#code-examples
            scheduler = BackgroundScheduler()
            job = scheduler.add_job(
                fetch_gmail_receipts, 'interval', minutes=5)
            scheduler.start()
