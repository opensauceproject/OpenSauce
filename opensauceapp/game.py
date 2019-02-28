from .Lobby import Lobby

class Game:
    # Singleton
    instance = None

    @staticmethod
    def get_instance():
        if not Game.instance:
            Game.instance = Game()
        return Game.instance

    def __init__(self):
        self.lobby = {}

    def __str__(self):
        s = "Game State : \n"
        if len(self.lobby) <= 0:
            s += "No room available !"
        for lobbyName, lobby in self.lobby.items():
            s += str(lobby) + "\n"
        return s

    def get_lobby_list(self):
        return self.lobby

    def get_lobby(self, lobbyName):
        if lobbyName not in self.lobby:
            self.lobby[lobbyName] = Lobby(lobbyName)
        return self.lobby[lobbyName]

    def remove_lobby(self, lobbyName):
        del self.lobby[lobbyName]
