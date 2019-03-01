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
        self.lobbies = {}

    def __str__(self):
        s = "Game State : \n"
        if len(self.lobbies) <= 0:
            s += "No room available !"
        for lobbyName, lobby in self.lobbies.items():
            s += str(lobby) + "\n"
        return s

    def get_lobbies_list(self):
        return self.lobbies

    def get_lobby(self, lobbyName):
        if lobbyName not in self.lobbies:
            self.lobbies[lobbyName] = Lobby(lobbyName)
        return self.lobbies[lobbyName]

    def remove_lobby(self, lobbyName):
        del self.lobbies[lobbyName]
