from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Zone


class AllZonesView(APIView):

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        zones = [zone.serialize() for zone in zones]
        return Response(zones, status=200)


class ZonePKView(APIView):

    def get(self, request, *args, **kwargs):
        zone = Zone.objects.get(pk=self.kwargs["pk"])
        zone = zone.serialize()
        return Response(zone, status=200)
