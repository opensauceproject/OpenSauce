from channels.generic.websocket import WebsocketConsumer
from django.utils.html import escape
import json

from .Game import Game


class OpenSauceConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_name"]
        # convert from byte to string the secret key of the socket
        # to have a unique id that represent the player
        self.secKey = str(dict(self.scope["headers"])[
                          b'sec-websocket-key'])[2:-1]
        Game.get_instance().get_lobby(self.lobby_name).player_add(self.secKey, self)
        print(Game.get_instance())

    def disconnect(self, close_code):
        result = Game.get_instance().get_lobby(
            self.lobby_name).player_remove(self.secKey)
        if result:
            Game.get_instance().remove_lobby(self.lobby_name)
        print(Game.get_instance())

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)

        # type of the request
        type = data["type"]
        # print("$<" + self.secKey + "> " + str(data))

        lobby = Game.get_instance().get_lobby(self.lobby_name)

        # Evaluate the message
        if type == "join":
            lobby.player_join(self.secKey, escape(data["pseudo"]))
        elif type == "leave":
            lobby.player_leave(self.secKey)
        elif type == "submit":
            lobby.player_submit(self.secKey, data["answer"])
        elif type == "settings":
            lobby.set_settings(data["settings"])

        print(Game.get_instance())
