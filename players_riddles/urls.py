from django.urls import path
from .views import PlayersRiddlesView

app_name = "players_riddles"

urlpatterns = [
    path("player/", PlayersRiddlesView.as_view(), name="players_riddles_view")

]
