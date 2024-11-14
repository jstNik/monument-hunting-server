import secrets

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import extract_api_key, client_not_authorized
from monument_hunting.settings import env
from .models import Zone


class AllZonesView(APIView):

    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        zones = Zone.objects.all()
        zones = [zone.serialize() for zone in zones]
        return Response(zones, status=status.HTTP_200_OK)


class ZonePKView(APIView):

    def get(self, request, *args, **kwargs):
        api_key = extract_api_key(request)
        if api_key != env("API_KEY"):
            return client_not_authorized()
        zone_pk = self.kwargs.get("pk")
        zone = Zone.objects.get(pk=zone_pk)
        zone = zone.serialize()
        return Response(zone, status=status.HTTP_200_OK )
