from celery import Celery

app = Celery()
from ProductImporter import celery_app
from django.conf import settings


@celery_app.task(max_retries=settings.CELERY_EVENT_MAX_RETRIES, ignore_result=False)
def send_sms(sms_from, sms_to, message, template_dict):
   pass