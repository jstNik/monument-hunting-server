import secrets

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from monument_hunting.settings import env
from .models import Zone


class AllZonesView(APIView):

    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        zones = Zone.objects.all()
        zones = [zone.serialize() for zone in zones]
        return Response(zones, status=status.HTTP_200_OK)


class ZonePKView(APIView):

    def get(self, request, *args, **kwargs):
        api_key = request.headers.get["api_key"]
        if api_key != env("API_KEY"):
            return Response(
                {"error": "Your client is not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        zone = Zone.objects.get(pk=self.kwargs["pk"])
        zone = zone.serialize()
        return Response(zone, status=status.HTTP_200_OK )
