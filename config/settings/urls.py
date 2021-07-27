from django.conf.urls import include, url
from ProductImporter.user.views import index


urlpatterns = [
    url(r'', index, name='index'),
]
