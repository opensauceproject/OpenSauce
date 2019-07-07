from django.conf.urls import url

from .game.OpenSauceConsumer import OpenSauceConsumer
from .websockets.UpdateLobbiesConsumer import UpdateLobbiesConsumer

websocket_urlpatterns = [
    url(r'^lobby/(?P<lobby_name>[^/]+)/', OpenSauceConsumer),
    url(r'^index/', UpdateLobbiesConsumer),
]
