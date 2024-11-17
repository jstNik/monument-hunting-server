from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import invalid_id
from riddles.models import Riddle
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
        player_riddles = PlayersRiddles.objects.prefetch_related("riddle").filter(player_id=player_pk)
        riddles = Riddle.objects.all()
        if not player_riddles:
            return Response([], status=status.HTTP_200_OK)
        player_riddles = [pr.serialize() for pr in player_riddles]
        riddles = [r.serialize() for r in riddles]
        return Response(
            {
                "player_riddles": player_riddles,
                "riddles": riddles
            },
            status=status.HTTP_200_OK
        )
