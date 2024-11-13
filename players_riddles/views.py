from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from monument_hunting.settings import env
from .models import PlayersRiddles


class PlayersRiddlesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        player_pk = self.kwargs["pk"]
        riddles = PlayersRiddles.objects.select_related("riddle").filter(player__id=player_pk)
        riddles = [pr.serialize() for pr in riddles]
        return Response(riddles, status=status.HTTP_200_OK)
