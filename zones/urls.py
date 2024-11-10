from django.urls import path

from .views import *

app_name = "zones"

urlpatterns = [
    path("all/", AllZonesView.as_view(), name="all_zones"),
    path("<int:pk>/", ZonePKView.as_view(), name="zone"),
]
