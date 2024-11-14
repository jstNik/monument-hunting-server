from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import extract_api_key, client_not_authorized, invalid_id
from monument_hunting.settings import env
from .models import PlayersRiddles


class PlayersRiddlesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        player_pk = self.kwargs.get("pk")
        if player_pk is None:
            invalid_id()
        riddles = PlayersRiddles.objects.select_related("riddle").filter(player__id=player_pk)
        riddles = [pr.serialize() for pr in riddles]
        return Response(riddles, status=status.HTTP_200_OK)
