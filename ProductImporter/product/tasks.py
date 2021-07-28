from celery import Celery

from ProductImporter.common.base_tasks import TransactionAwareTask
from ProductImporter.product.models import ProductUploader, PENDING, Product, COMPLETED

app = Celery()
from ProductImporter import celery_app
from django.conf import settings
import pandas as pd
from django.utils import timezone
from django import db
MAX_RECORD_TO_PROCESS_IN_ONE_BATCH = 5000


@celery_app.task(base=TransactionAwareTask, bind=True,
             max_retries=settings.CELERY_EVENT_MAX_RETRIES, ignore_result=False)
def import_product(self, uploader_id):
    uploader = ProductUploader.objects.filter(id=uploader_id, status=PENDING).first()
    if not uploader:
        return
    uploader.started_at = timezone.now()
    url = uploader.link
    data = pd.read_csv(url)
    data.drop_duplicates(subset="sku", keep='last', inplace=True)
    sku_names = data['sku'].unique().tolist()
    records = Product.objects.filter(sku__in=sku_names).order_by(
        'id').only('name', 'description')
    total_rec = records.count()

    # update existsing records
    sku_names_ = []
    batch_count = 0
    count = 0
    update_list = []
    for record in records.iterator():
        count += 1
        batch_count += 1
        sku_names_.append(record.sku)
        update_list.append(Product(
            id=record.id,
            name=data.loc[data['sku'] == record.sku, 'name'],
            sku=data.loc[data['sku'] == record.sku, 'description']
        ))

        if batch_count == MAX_RECORD_TO_PROCESS_IN_ONE_BATCH or count == total_rec:
            # exclude the updated record from dataframe
            data = data[~(data.sku.isin(sku_names_))]
            Product.objects.bulk_update(update_list, ['name', 'description'])
            db.reset_queries()
            update_list = []
            batch_count = 0

    # create new records
    product_list = []
    count = 0
    batch_count = 0
    total_rec = len(data.index)
    for row in data.itertuples():
        count += 1
        batch_count += 1
        product_list.append(Product(
            batch=uploader, name=row[1],
            sku=row[2], description=row[3],
            is_active=True
        ))

        if batch_count == MAX_RECORD_TO_PROCESS_IN_ONE_BATCH or count == total_rec:
            Product.objects.bulk_create(product_list)
            product_list = []
            batch_count = 0
            db.reset_queries()

    db.reset_queries()
    uploader.status = COMPLETED
    uploader.completed_at = timezone.now()
    uploader.save()


