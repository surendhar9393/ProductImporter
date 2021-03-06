# Generated by Django 3.0 on 2021-07-25 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productuploader',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.ProductUploader'),
        ),
    ]
