from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from monument_hunting.settings import env
from .models import Riddle
from .models import Monument


class RiddlesInZone(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        zone_pk = self.kwargs["zone_pk"]
        riddles = Riddle.objects.select_related("monument__zone").filter(monument__zone__id=zone_pk)
        riddles = [riddle.serialize() for riddle in riddles]
        return Response(riddles, status=status.HTTP_200_OK)
