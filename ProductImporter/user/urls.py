from django.conf.urls import url
from ProductImporter.user.views import Login

urlpatterns = [
    url(r'^user/login',  Login.as_view(), name='login-api'),
]

