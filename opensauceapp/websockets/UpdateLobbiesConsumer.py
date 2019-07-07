from channels.generic.websocket import WebsocketConsumer
from django.utils.html import escape
import json

class UpdateLobbiesConsumer(WebsocketConsumer):
    open_sockets = []

    @staticmethod
    def update_open_sockets():
        open_sockets = UpdateLobbiesConsumer.open_sockets[:]
        if len(open_sockets) > 0:
            lobbies_list = UpdateLobbiesConsumer.lobbies_list()
            for socket in open_sockets:
                socket.send(text_data=lobbies_list)

    @staticmethod
    def lobbies_list():
        data = {"list": []}
        from opensauceapp.game.Game import Game
        lobbies = Game.get_instance().get_lobbies_list()
        for lobbyname, lobby in lobbies.items():
            total_count = lobby.count()
            l = {
                "name": lobby.name,
                "total": total_count,
                "players": lobby.count_players(),
                "spectators": lobby.count_spectators(),
                "password": lobby.settings["password"] != "",
                "max_players": lobby.settings["max_players"],
            }
            data["list"].append(l)

        data["list"] = sorted(
            data["list"], key=lambda d: (-d["total"], -d["players"], -d["spectators"]))

        return json.dumps(data)

    def connect(self):
        self.accept()
        self.send(text_data=UpdateLobbiesConsumer.lobbies_list())
        self.open_sockets.append(self)

    def disconnect(self, close_code):
        self.open_sockets.remove(self)
