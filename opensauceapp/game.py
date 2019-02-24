import random
import datetime
from threading import Thread
from time import sleep
import json
from asgiref.sync import async_to_sync


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

    sauces = [("q1", "1"), ("q2", "2"), ("q3", "3")]

    timeAvailableToAnswer = datetime.timedelta(seconds=5)
    timeoutWhenChangingRound = datetime.timedelta(seconds=3)
    timeoutWhenGameFinished = datetime.timedelta(seconds=5)

    # the last is repeated for all the next players
    pointsRepartition = [5, 3, 2, 1]

    def __init__(self, name):
        self.name = name
        self.players = {}
        self.settings = {}
        self.questionID = 0
        self.currentSauce = None
        self.questionDateTimeEnd = None
        self.playerThatFound = None
        self.nextRound()

    def playerAdd(self, secKey, socket):
        print("player add")
        self.players[secKey] = Player(socket)
        self.sendUpdate()

    def playerRemove(self, secKey):
        print("player remove")
        if secKey in self.players:
            del self.players[secKey]
        # if the last player is remove the lobby is also removed
        if self.count() <= 0:
            Game.getInstance().removeLobby(self.name)
        self.sendUpdate()

    def count(self):
        return len(self.players)

    def playerJoin(self, secKey, playerName):
        print("player join")
        player = self.players[secKey]
        player.isPlaying = True
        player.name = playerName
        self.sendUpdate()

    def playerLeave(self, secKey):
        print("player leave")
        player = self.players[secKey]
        player.isPlaying = False
        self.sendUpdate()

    def getAndSetCurrentPointsIndex(self, player):
        index = len(self.playerThatFound)
        lenPointsRepartitionMinusOne = len(Lobby.pointsRepartition) - 1
        if index >= lenPointsRepartitionMinusOne:
            index = lenPointsRepartitionMinusOne

        self.playerThatFound.append(player)
        player.addPointsRound(Lobby.pointsRepartition[index])

    def playerSubmit(self, secKey, answer):
        player = self.players[secKey]
        if not player.canEarnPoints():
            return

        if answer == self.currentSauce[1]:
            # right answer
            self.getAndSetCurrentPointsIndex(player)
            self.changeRoundIfShould()
            self.sendUpdate()

    def changeRoundIfShould(self):
        # if a player can earn points the round is still active
        for player in self.players.values():
            if player.canEarnPoints():
                return

        self.nextRound()
        self.sendUpdate()

    def nextRound(self):
        self.questionID += 1
        # reset players
        for player in self.players.values():
            player.resetRound()
        # set new sauce
        self.currentSauce = random.choice(Lobby.sauces)
        # reset play that found
        self.playerThatFound = []
        # set new end time
        self.questionDateTimeEnd = datetime.datetime.now() + Lobby.timeAvailableToAnswer
        # thread = Thread(target=self.giveAnswerAfterDelay, args=(self.questionID,))
        # thread.start()

    def __str__(self):
        s = "--" + self.name + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s

    def giveAnswerAfterDelay(self, questionID):
        sleep(Lobby.timeAvailableToAnswer.total_seconds())
        # is it still the same round ?
        if questionID == self.questionID:
            self.sendAnswer()

    def sendUpdate(self):
        print("send update")
        data = {"type": "game_state", "state": self.getStatus()}
        self.sendToEveryPlayers(data)

    def sendAnswer(self):
        print("send answer")
        data = {"type": "answer", "answer": self.currentSauce[1], "timeoutChangingRoundDateTimeEnd" : datetime.datetime.now() + Lobby.timeoutWhenChangingRound}
        self.sendToEveryPlayers(data)

    def sendToEveryPlayers(self, data):
        for player in self.players.values():
            player.socket.send(text_data=json.dumps(data))


    def getStatus(self):
        status = {}
        status["name"] = self.name
        players = []
        for player in self.players.values():
            if player.isPlaying:
                players.append(player.getStatus())
        # sorted by score
        status["players"] = list(sorted(players, key=lambda x: -x["score"]))
        status["currentQuestion"] = self.currentSauce[0]
        status["questionDateTimeEnd"] = self.questionDateTimeEnd.isoformat()
        return status


class Player:
    def __init__(self, socket):
        self.socket = socket
        self.isPlaying = False
        self.name = None
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
        s = ""
        if self.name:
            s += self.name + " "
        if not self.isPlaying:
            s += "(spectating)"
        else:
            s += str(self.score)
        return s

    def getStatus(self):
        status = {}
        status["name"] = self.name
        status["score"] = self.score
        status["pointsThisRound"] = self.pointsThisRound
        return status
