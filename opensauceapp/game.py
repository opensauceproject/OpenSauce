import random
import datetime

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

    sauces = [("q1", "a1"), ("q2", "a2"), ("q3", "a3")]

    timeAvailableToAnswer = datetime.timedelta(seconds=15)

    # the last is repeated for all the next players
    pointsRepartition = [5, 3, 2, 1]

    def __init__(self, name):
        self.name = name
        self.players = {}
        self.settings = {}
        self.currentSauce = None
        self.questionDateTimeEnd = None
        self.currentPointsIndex = None
        self.nextRound()

    def count(self):
        return len(self.players)

    def getAndSetCurrentPointsIndex(self):
        index = self.currentPointsIndex
        lenPointsRepartitionMinusOne = len(Lobby.pointsRepartition) - 1
        if self.currentPointsIndex >= lenPointsRepartitionMinusOne:
            index = lenPointsRepartitionMinusOne

        self.currentPointsIndex += 1

        return Lobby.pointsRepartition[index]

    def addPlayer(self, secKey, playerName):
        self.players[secKey] = Player(playerName)

    def removePlayer(self, secKey):
        del self.players[secKey]
        # if the last player is remove the lobby is also removed
        if self.count() <= 0:
            Game.getInstance().removeLobby(self.name)

    def submit(self, secKey, answer):
        player = self.players[secKey]
        if not player.canEarnPoints():
            return False

        if answer == self.currentSauce[1]:
            player.addPointsRound(self.getAndSetCurrentPointsIndex())
            self.changeRoundIfShould()
            return True # true : tell other players that his score has been updated

        return False

    def changeRoundIfShould(self):
        # if a player can earn points the round is still active
        for player in self.players.values():
            if player.canEarnPoints():
                return False

        self.nextRound()
        return True

    def nextRound(self):
        self.resetPlayers()
        self.pickRandomNewSauce()
        self.setNewDateTimeEnd()
        self.resetPointsIndex()

    def resetPointsIndex(self):
        self.currentPointsIndex = 0

    def setNewDateTimeEnd(self):
        self.questionDateTimeEnd = datetime.datetime.now() + Lobby.timeAvailableToAnswer

    def pickRandomNewSauce(self):
        self.currentSauce = random.choice(Lobby.sauces)

    def resetPlayers(self):
        for player in self.players.values():
            player.resetRound()

    def __str__(self):
        s = "--" + self.name + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s

    def getStatus(self):
        status = {}
        status["name"] = self.name
        players = []
        for player in self.players.values():
            players.append(player.getStatus())
        # sorted by score
        status["players"] = list(sorted(players,  key=lambda x: -x["score"]))
        status["currentQuestion"] = self.currentSauce[0]
        status["questionDateTimeEnd"] = self.questionDateTimeEnd.isoformat()
        return status


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        # -1 : not found yet
        self.pointsThisRound = None
        self.resetRound()

    def canEarnPoints(self):
        return self.pointsThisRound < 0

    def resetRound(self):
        self.pointsThisRound = -1

    def addPointsRound(self, points):
        if self.canEarnPoints():
            self.pointsThisRound = points
            self.score += points

    def __str__(self):
        return self.name + " " + str(self.score)

    def getStatus(self):
        status = {}
        status["name"] = self.name
        status["score"] = self.score
        status["pointsThisRound"] = self.pointsThisRound
        return status
