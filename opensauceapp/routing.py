from django.conf.urls import url

from .game.OpenSauceConsumer import OpenSauceConsumer

websocket_urlpatterns = [
    url(r'^lobby/(?P<lobby_name>[^/]+)/', OpenSauceConsumer),
]
