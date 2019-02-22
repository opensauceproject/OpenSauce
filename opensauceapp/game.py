class Game:

    # Singleton
    instance = None

    @staticmethod
    def getInstance():
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

    def getLobbyList(self):
        return self.lobby

    def getLobby(self, lobbyName):
        if lobbyName not in self.lobby:
            self.lobby[lobbyName] = Lobby(lobbyName)
        return self.lobby[lobbyName]

    def removeLobby(self, lobbyName):
        del self.lobby[lobbyName]


class Lobby:
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.settings = {}

    def count(self):
        return len(self.players)

    def addPlayer(self, secKey, playerName):
        self.players[secKey] = Player(playerName)

    def removePlayer(self, secKey):
        del self.players[secKey]
        # if the last player is remove the lobby is also removed
        if self.count() <= 0:
            Game.getInstance().removeLobby(self.name)

    def submit(self, secKey, answer):
        print(answer)

    def __str__(self):
        s = "--" + self.name + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def __str__(self):
        return self.name + " " + str(self.score)
