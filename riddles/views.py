from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import extract_api_key, client_not_authorized, invalid_id
from monument_hunting.settings import env
from .models import Riddle
from .models import Monument


class RiddlesInZone(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        zone_pk = self.kwargs.get("zone_pk")
        if zone_pk is None:
            return invalid_id()
        riddles = Riddle.objects.select_related("monument__zone").filter(monument__zone__id=zone_pk)
        riddles = [riddle.serialize() for riddle in riddles]
        return Response(riddles, status=status.HTTP_200_OK)
