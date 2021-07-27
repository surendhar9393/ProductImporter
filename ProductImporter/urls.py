from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
# import debug_toolbar
from ProductImporter.user.views import index

from django.conf.urls.static import static
from django.conf import settings

# local imports
from ProductImporter.user import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'', index, name='index'),
    # url(r'^__debug__/', include(debug_toolbar.urls)),

]
