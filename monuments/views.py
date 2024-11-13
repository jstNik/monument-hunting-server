from os import environ

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from monument_hunting.settings import env
from .models import Monument


class MonumentsInZone(APIView):

    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        zone_pk = self.kwargs["zone_pk"]
        monuments = Monument.objects.select_related("zone").filter(zone_id=zone_pk)
        monuments = [monument.serialize() for monument in monuments]
        return Response(monuments, status=status.HTTP_200_OK)

