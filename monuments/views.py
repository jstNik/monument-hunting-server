from os import environ

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import extract_api_key, client_not_authorized, invalid_id
from monument_hunting.settings import env
from .models import Monument


class MonumentsInZone(APIView):

    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        zone_pk = self.kwargs.get("zone_pk")
        if zone_pk is None:
            return invalid_id()
        monuments = Monument.objects.select_related("zone").filter(zone_id=zone_pk)
        monuments = [monument.serialize() for monument in monuments]
        return Response(monuments, status=status.HTTP_200_OK)

