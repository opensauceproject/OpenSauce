from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'lobby/(?P<lobby_name>[^/]+)/', consumers.OpenSauceConsumer),
]
