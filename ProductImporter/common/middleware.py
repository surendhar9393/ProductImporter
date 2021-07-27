from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        return request.META.get('HTTP_TOKEN')