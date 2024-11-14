import re

import jwt
from django.contrib.auth.hashers import make_password
from django.contrib.gis.gdal.prototypes.srs import get_auth_code
from django.core.exceptions import ValidationError
from django.shortcuts import render
from gunicorn.config import validate_user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from django.core.validators import validate_email

from common.utils import extract_api_key, client_not_authorized, invalid_credentials
from monument_hunting.settings import env, SECRET_KEY
from .models import Player


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        username = request.data.get("username")
        password = request.data.get("password")
        player = authenticate(username=username, password=password)
        if player is not None:
            return get_auth_code(player)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):

    def post(self, request):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]

        if username is None or password is None or email is None:
            return Response(
                {"error": "All fields are mandatory"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Player.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_409_CONFLICT
            )

        if len(password) < 8 or not re.compile(r"\w").match(password) or re.compile(r"\s").match(password):
            return Response(
                {"error": "Password is too weak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError as _:
            return Response(
                {"error": "Bad email"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            player = Player.objects.create(
                username=username,
                password=make_password(password),
                email=email
            )
            refresh = RefreshToken.for_user(player)
            decode_access = jwt.decode(str(refresh.access_token), SECRET_KEY, algorithms=["HS256"])
            decode_refresh = jwt.decode(str(refresh), SECRET_KEY, algorithms=["HS256"])
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "access_expiration": decode_access.get("exp"),
                    "refresh_token": str(refresh),
                    "refresh_expiration": decode_refresh.get("exp")
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenRefreshView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                decode_access = jwt.decode(str(refresh.access_token), SECRET_KEY, algorithms=["HS256"])
                decode_refresh = jwt.decode(str(refresh), SECRET_KEY, algorithms=["HS256"])
                return Response(
                    {
                        "access_token": str(refresh.access_token),
                        "access_expiration": decode_access.get("exp"),
                        "refresh_token": str(refresh),
                        "refresh_expiration": decode_refresh.get("exp")
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": "Refresh token is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
