from channels.generic.websocket import WebsocketConsumer
from django.utils.html import escape
import json

class UpdateLobbiesConsumer(WebsocketConsumer):
    open_sockets = []

    @staticmethod
    def update_open_sockets():
        lobbies_list = UpdateLobbiesConsumer.lobbies_list()
        for socket in UpdateLobbiesConsumer.open_sockets:
            socket.send(text_data=lobbies_list)

    def connect(self):
        print("websocket connect")
        self.accept()
        self.send(text_data=UpdateLobbiesConsumer.lobbies_list())
        self.open_sockets.append(self)

    def disconnect(self, close_code):
        print("websocket disconnect")
        self.open_sockets.remove(self)

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
                "password": lobby.settings["password"] != ""
            }
            data["list"].append(l)

        data["list"] = sorted(
            data["list"], key=lambda d: (-d["total"], -d["players"], -d["spectators"]))

        return json.dumps(data)
