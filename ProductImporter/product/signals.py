from django.dispatch import receiver
from django.db.models.signals import post_save
from ProductImporter.product.models import ProductUploader
from ProductImporter.product.tasks import import_product
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=ProductUploader)
def trigger_invoice_creation_past(sender, instance, created, **kwargs):
    if created:
        import_product.apply_async((instance.id,), eta=timezone.now() + timedelta(seconds=5))
