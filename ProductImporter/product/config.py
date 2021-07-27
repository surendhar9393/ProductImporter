from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'ProductImporter.product'

    def ready(self):
        import ProductImporter.product.signals

