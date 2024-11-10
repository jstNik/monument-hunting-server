from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Monument


class MonumentsInZone(APIView):

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        zone_pk = self.kwargs["zone_pk"]
        monuments = Monument.objects.select_related("zone").filter(zone_id=zone_pk)
        monuments = [monument.serialize() for monument in monuments]
        return Response(monuments, status=200)
