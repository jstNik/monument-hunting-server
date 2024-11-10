from django.urls import path

from .views import MonumentsInZone

app_name = "monuments"

urlpatterns = [
    path("zone/<int:zone_pk>/", MonumentsInZone.as_view(), name="monument_in_zone")
]
