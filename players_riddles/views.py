from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import invalid_id
from players.models import Player
from riddles.models import Riddle
from zones.models import Zone
from .models import PlayersRiddles


class PlayersRiddlesView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # api_key = extract_api_key(request)
        # if api_key != env("API_KEY"):
        #     return client_not_authorized()
        player_pk = self.kwargs.get("pk")
        if player_pk is None:
            return invalid_id()
        player = Player.objects.get(id=player_pk)
        player_riddles = PlayersRiddles.objects.prefetch_related("riddle").filter(player_id=player_pk)
        if player.zone is None:
            riddles = Riddle.objects.all()
        else:
            riddles = Riddle.objects.all().filter(zone_id=player.zone_id)
        zones = Zone.objects.all()
        if not player_riddles:
            return Response([], status=status.HTTP_200_OK)
        player_riddles = [pr.serialize() for pr in player_riddles]
        riddles = [r.serialize() for r in riddles]
        zones = [z.serialize() for z in zones]
        return Response(
            {
                "player": player.serialize(),
                "player_riddles": player_riddles,
                "riddles": riddles,
                "zones": zones
            },
            status=status.HTTP_200_OK
        )
