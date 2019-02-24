from channels.generic.websocket import WebsocketConsumer
from django.utils.html import escape
import json

from .game import *


class OpenSauceConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_name"]
        # convert from byte to string the secret key of the socket
        # to have a unique id that represent the player
        self.secKey = str(dict(self.scope["headers"])[b'sec-websocket-key'])[2:-1]
        Game.getInstance().getLobby(self.lobby_name).playerAdd(self.secKey, self)

        print(Game.getInstance())

    def disconnect(self, close_code):
        Game.getInstance().getLobby(self.lobby_name).playerRemove(self.secKey)
        print(Game.getInstance())

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)

        # type of the request
        type = data["type"]
        print("$<" + self.secKey + "> " + str(data))

        lobby = Game.getInstance().getLobby(self.lobby_name)

        # Evaluate the message
        if type == "join":
            lobby.playerJoin(self.secKey, escape(data["pseudo"]))
        elif type == "leave":
            lobby.playerLeave(self.secKey)
        elif type == "submit":
            lobby.playerSubmit(self.secKey, data["answer"])

        print(Game.getInstance())
