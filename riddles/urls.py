from django.urls import path

from .views import RiddlesInZone

app_name = "riddles"

urlpatterns = [
    path("zone/<int:zone_pk>/", RiddlesInZone.as_view(), name="riddles_in_zone")
]
