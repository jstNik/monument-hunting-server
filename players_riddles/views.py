from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from common.utils import invalid_id, extract_api_key, client_not_authorized
from monument_hunting.settings import env
from .models import PlayersRiddles
from .utils import response_data


class PlayersRiddlesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        player_pk = self.request.user.id
        if player_pk is None:
            return invalid_id()
        return response_data(player_pk)

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
        return response_data(request.user.id)