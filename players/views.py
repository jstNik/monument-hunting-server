import re

import jwt
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from gunicorn.config import validate_user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from django.core.validators import validate_email

from monument_hunting.settings import env
from .models import Player


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        username = request.data["username"]
        password = request.data["password"]
        player = authenticate(
            username=username, password=password)
        if player is not None:
            refresh = RefreshToken.for_user(player)
            decode_access = jwt.decode(str(refresh.access_token), options={"verify_signature": False})
            decode_refresh = jwt.decode(str(refresh), options={"verify_signature": False})
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "access_expiration": decode_access.get("exp"),
                    "refresh_token": str(refresh),
                    "refresh_expiration": decode_refresh.get("exp")
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class SignupView(APIView):

    def post(self, request):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

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
            decode_access = jwt.decode(str(refresh.access_token), options={"verify_signature": False})
            decode_refresh = jwt.decode(str(refresh), options={"verify_signature": False})
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
