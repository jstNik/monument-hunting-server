from rest_framework import status
from rest_framework.response import Response

from players.models import Player
from players_riddles.models import PlayersRiddles
from regions.models import Region
from riddles.models import Riddle
from zones.models import Zone


def response_data(player_pk):
    player = Player.objects.get(id=player_pk)
    player_riddles = PlayersRiddles.objects.prefetch_related("riddle").filter(player_id=player_pk)
    zones = Zone.objects.all()
    regions = Region.objects.all()
    riddles = Riddle.objects.all()
    if not player_riddles:
        player_riddles = []
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