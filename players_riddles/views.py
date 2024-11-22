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
from .utils import responseData


class PlayersRiddlesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        player_pk = self.request.user.id
        if player_pk is None:
            return invalid_id()
        return responseData(player_pk)

    def post(self, request):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        riddle_completed = request.data.get("riddle_id")
        if riddle_completed is None:
            return invalid_id()
        PlayersRiddles.objects.create(
            player_id=request.user.id,
            riddle_id = riddle_completed
        )
        return responseData(request.user.id)