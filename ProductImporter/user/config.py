from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'ProductImporter.user'

    def ready(self):
        pass

