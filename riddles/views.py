from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Riddle
from .models import Monument


class RiddlesInZone(APIView):

    def get(self, request, *args, **kwargs):
        zone_pk = self.kwargs["zone_pk"]
        riddles = Riddle.objects.select_related("monument__zone").filter(monument__zone__id=zone_pk)
        riddles = [riddle.serialize() for riddle in riddles]
        return Response(riddles, status=200)
