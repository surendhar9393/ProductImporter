from rest_framework.response import Response
from rest_framework import status, generics
from ProductImporter.common.middleware import CsrfExemptSessionAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.settings import api_settings

from ProductImporter.user.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@permission_classes([])
class Login(generics.CreateAPIView):
    # overriding the authentication class and permission class
    # to allow user to login
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)

    def generate_auth_token(self, user):
        # Generating the JWT Token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            resp = {
                "message": "Email and password are required"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp)
        user = User.objects.do_login(
            request=request, user_name=email, password=password)
        if user:
            login(request, user)
            token = self.generate_auth_token(user)

            resp = {
                "token": token,
                "name": user.name,
                "email": user.email
            }
            return Response(status=status.HTTP_200_OK, data=resp)
        resp = {
            "message": "Invalid User Name and Password"
        }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=resp)


def index(request):
    return render(request, 'index.html')