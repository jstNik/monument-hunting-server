from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import invalid_id, extract_api_key, client_not_authorized
from monument_hunting.settings import env
from players.models import Player
from regions.models import Region
from riddles.models import Riddle
from zones.models import Zone
from .models import PlayersRiddles


class PlayersRiddlesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        player_pk = self.kwargs.get("pk")
        if player_pk is None:
            return invalid_id()
        player = Player.objects.get(id=player_pk)
        player_riddles = PlayersRiddles.objects.prefetch_related("riddle").filter(player_id=player_pk)
        zones = Zone.objects.all()
        regions = Region.objects.all()
        riddles = Riddle.objects.all()
        if not player_riddles:
            player_riddles = [ ]
        player_riddles = [pr.serialize() for pr in player_riddles]
        riddles = [r.serialize() for r in riddles]
        zones = [z.serialize() for z in zones]
        regions = [r.serialize() for r in regions]
        return Response(
            {
                "player": player.serialize(),
                "player_riddles": player_riddles,
                "riddles": riddles,
                "zones": zones,
                "regions": regions
            },
            status=status.HTTP_200_OK
        )
