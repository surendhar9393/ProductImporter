from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import gettext_lazy as _

PENDING = 'Pending'
COMPLETED = 'Completed'
IN_PROGRESS = 'In-Progress'

STATUSES = (
    (PENDING, 'Pending'),
    (IN_PROGRESS, 'In-Progress'),
    (COMPLETED, 'Completed'),

)


class ProductUploader(models.Model):
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT)

    created_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(_("Status"), max_length=30, choices=STATUSES, default=PENDING,
                              help_text=_("Current status of document upload."))

    link = models.CharField(_('File URL'), max_length=255)

    started_at = models.DateTimeField(null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)


class Product(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)

    batch = models.ForeignKey(ProductUploader, on_delete=models.PROTECT)

    name = models.CharField(_('Name'), max_length=100)

    sku = models.CharField(_('Name'), max_length=100, unique=True)

    is_active = models.BooleanField(_('Is Active'), default=True)

    description = models.TextField(_('Description'), null=True, blank=True)




