from celery import Celery

from ProductImporter.product.models import ProductUploader, PENDING, Product, COMPLETED

app = Celery()
from ProductImporter import celery_app
from django.conf import settings
import pandas as pd
from django.utils import timezone
from django import db
MAX_RECORD_TO_PROCESS_IN_ONE_RUN = 5000

@celery_app.task(max_retries=settings.CELERY_EVENT_MAX_RETRIES, ignore_result=False)
def import_product(uploader_id):
    uploader = ProductUploader.objects.filter(id=uploader_id, status=PENDING).first()
    db.reset_queries()
    uploader.started_at = timezone.now()
    url = uploader.link
    data = pd.read_csv(url)
    data.drop_duplicates(subset="sku", keep='last', inplace=True)
    sku_names = data['sku'].unique().tolist()
    print("1b-")
    records = Product.objects.filter(sku__in=sku_names).only('name', 'description')
    print("1c---", records.count())
    total_rec = records.count()
    batches = int(total_rec/MAX_RECORD_TO_PROCESS_IN_ONE_RUN) + 1
    print("batch-", batches)
    for i in range(0, batches):
        records = Product.objects.filter(sku__in=sku_names).order_by(
            'id').only('name', 'description')[i*MAX_RECORD_TO_PROCESS_IN_ONE_RUN:(i+1)*MAX_RECORD_TO_PROCESS_IN_ONE_RUN]
        print("reco00000000000")
        for record in records.iterator():
            # loop to update the existing records
            # writing to DB using bulk update method
            record.name = data.loc[data['sku'] == record.sku, 'name']
            # sku_val_mapping.get(record.sku)[0]
            sku_names.append(record.sku)
            record.description = data.loc[data['sku'] == record.sku, 'description']


        print("1d---")
        if records:
            print("1e--")
            data = data[~(data.sku.isin([sku_names]))]
            Product.objects.bulk_update(records, ['name', 'description'])
            print("1f--")
            # db.reset_queries()

    print("1e---")
    product_list = []
    count = 0
    for row in data.itertuples():
        count += 1
        product_list.append(Product(
            batch=uploader, name=row[1],
            sku=row[2], description=row[3],
            is_active=True
        ))
        if count >= MAX_RECORD_TO_PROCESS_IN_ONE_RUN:
            Product.objects.bulk_create(product_list)
            product_list = []
            db.reset_queries()

    db.reset_queries()
    print("3---------")
    uploader.status = COMPLETED
    uploader.completed_at = timezone.now()
    uploader.save()


