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
from common.utils import client_not_authorized, extract_api_key
from monument_hunting.settings import env
from .models import Player
from .utils import generate_auth_token


class LoginView(APIView):

    permission_classes = []

    def post(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        username = request.data.get("username")
        password = request.data.get("password")
        player = authenticate(
            username=username, password=password
        )
        if player is not None and type(player) is Player:
            refresh: RefreshToken = RefreshToken.for_user(player)
            res = {
                "player": player.serialize(),
                "auth_token": generate_auth_token(refresh)
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class SignupView(APIView):

    permission_classes = []

    def post(self, request):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        username = request.data.get("username")
        if username == "":
            username = None
        password = request.data.get("password")
        if password == "":
            password = None
        email = request.data.get("email")
        if email == "":
            email = None

        if username is None or password is None or email is None:
            return Response(
                {"error": "All fields are mandatory"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(username) < 3:
            return Response(
                {"error": "Username must be 3 o more characters long"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if re.compile(r"\W").match(username):
            return Response(
                {"error": "Username can only contain letters, numbers and _"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Player.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_409_CONFLICT
            )

        if len(password) < 8 or re.compile(r"\W").match(password) or re.compile(r"\s").match(password):
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
            refresh: RefreshToken = RefreshToken.for_user(player)
            res = {
                "auth_token": generate_auth_token(refresh),
                "player": player.serialize()
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenRefreshView(APIView):

    permission_classes = []

    def post(self, request):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                player_id = refresh.get("user_id")
                if player_id is None:
                    return Response(
                        {"error": "Could not retrieve player id"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                player = Player.objects.get(id=player_id)
                if player is None:
                    return Response(
                        {"error": "Player id is not valid"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "auth_token": generate_auth_token(refresh),
                        "player": player.serialize()
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


class TokenVerifyView(APIView):

    permission_classes = []

    def post(self, request):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized("Api key not valid")
        token = request.data.get("access_token")
        if token is None:
            return client_not_authorized("Token has not been provided.")

        try:
            verify = AccessToken(token)
            player_id = verify.get("user_id")
            if player_id is None:
                return client_not_authorized("Could not find an id inside the token")
            player = Player.objects.get(id=player_id)
            if player is None:
                return client_not_authorized("Decoded id is not valid")
            return Response(
                player.serialize(),
                status=status.HTTP_200_OK
            )
        except Exception as _:
            return client_not_authorized("An error has occurred")
