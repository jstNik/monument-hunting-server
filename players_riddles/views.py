from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PlayersRiddles


class PlayersRiddlesView(APIView):

    def get(self, request, *args, **kwargs):
        player_pk = self.kwargs["pk"]
        riddles = PlayersRiddles.objects.select_related("riddle").filter(player__id=player_pk)
        riddles = [pr.serialize() for pr in riddles]
        return Response(riddles, status=200)
