from .Lobby import Lobby

from opensauceapp.websockets.UpdateLobbiesConsumer import UpdateLobbiesConsumer

class Game:
    # Singleton
    instance = None

    @staticmethod
    def get_instance():
        if not Game.instance:
            Game.instance = Game()
        return Game.instance

    def __init__(self):
        self.lobbies = {}

    def __str__(self):
        s = "Game State : \n"
        if len(self.lobbies) <= 0:
            s += "No room available !"
        for lobby_name, lobby in self.lobbies.items():
            s += str(lobby) + "\n"
        return s

    def get_lobbies_list(self):
        return dict(self.lobbies)

    def get_lobby(self, lobby_name):
        if not self.lobby_exist(lobby_name):
            self.lobbies[lobby_name] = Lobby(lobby_name)
        return self.lobbies[lobby_name]

    def lobby_exist(self, lobby_name):
        return lobby_name in self.lobbies

    def remove_lobby(self, lobby_name):
        del self.lobbies[lobby_name]
        UpdateLobbiesConsumer.update_open_sockets()
