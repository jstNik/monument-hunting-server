import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from monument_hunting.settings import SECRET_KEY


def generate_auth_token(refresh):
    decode_access = jwt.decode(str(refresh.access_token), SECRET_KEY, algorithms=["HS256"])
    decode_refresh = jwt.decode(str(refresh), SECRET_KEY, algorithms=["HS256"])
    return {
            "access_token": str(refresh.access_token),
            "access_expiration": decode_access.get("exp"),
            "refresh_token": str(refresh),
            "refresh_expiration": decode_refresh.get("exp")
        }
