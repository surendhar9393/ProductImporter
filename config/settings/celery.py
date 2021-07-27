from celery.schedules import crontab

beat_schedule = {
    # "import_product": {
    #     "task": "ProductImporter.product.tasks.send_sms",
    #     "schedule": crontab(hour="1", minute="30"),
    # },
}