from django.conf.urls import url

from .game.OpenSauceConsumer import OpenSauceConsumer

websocket_urlpatterns = [
    url(r'^ws/lobby/(?P<lobby_name>[^/]+)/', OpenSauceConsumer),
]
