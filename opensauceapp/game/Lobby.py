from .Player import Player

import random
import datetime
from threading import Thread
from time import sleep
import json
from asgiref.sync import async_to_sync


# TODO :
# - fix send when player join/leave/add/remove
# -

class Lobby:
    sauces = [
        {"question": "La réponse de cette super question de débug est tout simplement la touche UN du clavier !",
         "answer": "1",
         "category": "games",
         "type": "text"
         },
        {"question": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QBmRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAAQAAAATgAAAAAAAABgAAAAAQAAAGAAAAABcGFpbnQubmV0IDQuMS41AP/bAEMAGhITFxMQGhcVFx0bGh8nQConIyMnTzg8L0BdUmJhXFJaWWd0lH5nbYxvWVqBr4KMmZ6mp6ZkfLbDtKHBlKOmn//bAEMBGx0dJyInTCoqTJ9qWmqfn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn//AABEIAGQAZAMBIgACEQEDEQH/xAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4eLj5OXm5+jp6vHy8/T19vf4+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv/xAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4+Tl5ufo6ery8/T19vf4+fr/2gAMAwEAAhEDEQA/AOnooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiimTbvJfZ9/adv1oAp3+s2ennbNJuk/wCeacn/AOtWNL4vO79zaDHq7/0FZthoV7qLb2BijJ5kk6n6DvW5F4TslX97JNI3rkAUAVYvF53fvrQY9Uf/ABrdsNStdRQtbyZI+8h4YfhWFqPhVUhaSxkdmUZ8t+c/Q1z9pdS2V0k8JIZD+Y9KAPSKKZBKs8EcqfddQw/Gn0AFFFFABRRRQAUUUUAFFFFABRRRQAV51qaqmqXSoMKJWAH416BdXCWttJPIcLGuTXnYEl7d4UbpJn/UmgDu9FBGj2uf+eYq9UdvEILeOFekahR+AqSgAooooAKKKKACiiigAooooAKKK5rxFruwNZ2b/N0kkHb2HvQBV8TasLqX7JA2Yoz87D+Jv8BVnwrpRUfb5l5IxECPzaqGgaK1/KJ51ItkP/fZ9PpXaABVAUAAcADtQAtFFFABRRRQAUUUUAFFFFABRRVPVppINLuZIiQ6ocEdvegDJ8Q675Aa0tG/e9Hcfw+w96yNE0d9Tm3yZW3Q/M394+grKJycnk1oQa5qFvCkUM4SNBgKI14/SgDvI40ijWONQqKMADsKdXCf8JHqn/P1/wCQ1/wp3/CSap/z8D/v2v8AhQB3NFYXhrVLrUDcLcsH2bSGCgYzn0+lbtABRRRQAUUUUAFFFFABSEBlKsAQRgg96WigCt/Ztj/z5W//AH6X/Cj+zbH/AJ8rb/v0v+FWaKAKv9m2P/Plbf8Afpf8KP7Nsf8Anytv+/S/4VaooAjht4bcEQQxxA9Qihc/lUlFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/2Q==",
         "answer": "2",
         "category": "games",
         "type": "image"
         },
        {"question": "Question 3 : donc on réponds par la touche 3, simple non ?",
         "answer": "3",
         "category": "tv",
         "type": "text"
         },
    ]

    # States
    WAITING_FOR_PLAYERS = 0
    GAME_START_SOON = 1
    QUESTION = 2
    ANSWER = 3
    GAME_END = 4

    timeoutWhenGameStarting = datetime.timedelta(seconds=1)
    timeoutWhenQuestion = datetime.timedelta(seconds=15)
    timeoutWhenAnswer = datetime.timedelta(seconds=2)
    timeoutWhenGameFinished = datetime.timedelta(seconds=5)

    pointsGoal = 100

    minPlayers = 1

    # the last is repeated for all the next players
    pointsRepartition = [5, 3, 2, 1]

    def __init__(self, name):
        self.name = name
        self.settings = {}
        self.reset()

    def reset(self):
        self.state = Lobby.WAITING_FOR_PLAYERS
        self.players = {}
        self.gameStarted = False
        self.questionID = 0
        self.currentSauce = None
        self.datetime = datetime.datetime.now()
        self.playerThatFound = []
        self.history = []

    def count(self):
        return len(self.players)

    def get_players(self):
        return list(filter(lambda p: p.isPlaying, self.players.values()))

    def get_spectators(self):
        return list(filter(lambda p: not p.isPlaying, self.players.values()))

    def count_players(self):
        return len(self.get_players())

    def count_spectators(self):
        return len(self.get_spectators())

    def update_and_send_state(self):
        self.update_state()
        self.send_current_state()

    def game_start_soon_delay(self):
        self.datetime = datetime.datetime.now() + Lobby.timeoutWhenGameStarting
        sleep(Lobby.timeoutWhenGameStarting.total_seconds())
        self.next_round()
        self.send_question()

    def question_delay(self, questionID):
        self.datetime = datetime.datetime.now() + Lobby.timeoutWhenQuestion
        sleep(Lobby.timeoutWhenQuestion.total_seconds())
        # is it still the same round ?
        if questionID == self.questionID:
            self.answer()

    def answer(self):
        self.history.append((self.currentSauce, self.playerThatFound))
        self.questionID += 1
        self.send_answer()
        thread = Thread(target=self.answer_delay)
        thread.start()

    def get_best_player(self):
        playerSorted = sorted(self.get_players(), key=lambda p: p.score)
        if len(playerSorted) <= 0:
            return False
        else:
            return playerSorted[0]

    def answer_delay(self):
        self.datetime = datetime.datetime.now() + Lobby.timeoutWhenAnswer
        sleep(Lobby.timeoutWhenAnswer.total_seconds())
        best_player = self.get_best_player()
        if best_player and best_player.score >= Lobby.pointsGoal:
            self.send_game_end()
        else:
            self.next_round()
            self.send_question()

    def next_round(self):
        self.state = Lobby.QUESTION
        # reset players
        for player in self.players.values():
            player.reset_round()
        self.send_scoreboard()
        # set new sauce
        self.currentSauce = random.choice(Lobby.sauces)
        # reset play that found
        self.playerThatFound = []
        # set new end time
        thread = Thread(target=self.question_delay,
                        args=(self.questionID,))
        thread.start()

    def update_state(self):
        if Lobby.WAITING_FOR_PLAYERS == self.state:
            if self.count_players() >= Lobby.minPlayers:
                self.state = Lobby.GAME_START_SOON
                thread = Thread(target=self.game_start_soon_delay)
                thread.start()
        elif Lobby.GAME_START_SOON == self.state:
            pass
        elif Lobby.QUESTION == self.state:
            if len(self.playerThatFound) >= self.count_players():
                self.state = Lobby.ANSWER
                self.datetime = datetime.datetime.now() + Lobby.timeoutWhenQuestion
        elif Lobby.ANSWER == self.state:
            pass
        elif Lobby.GAME_END == self.state:
            pass
        else:
            raise "Unhandled state"

    def send_current_state(self):
        if Lobby.WAITING_FOR_PLAYERS == self.state:
            self.send_waiting_for_players()
        elif Lobby.GAME_START_SOON == self.state:
            self.send_game_starts_soon()
        elif self.state == Lobby.QUESTION:
            self.send_question()
        elif Lobby.ANSWER == self.state:
            self.send_answer()
        elif Lobby.GAME_END == self.state:
            self.send_game_end()
        else:
            raise "Unhandled state"

    def player_add(self, secKey, socket):
        player = Player(socket)
        if len(self.players) < 1:
            player.isOwner = True
        self.players[secKey] = player
        self.send_scoreboard()
        self.update_and_send_state()

    def player_remove(self, secKey):
        if secKey in self.players:
            del self.players[secKey]
        # if the last player is remove the lobby tell to remove the lobby
        self.send_scoreboard()
        self.update_and_send_state()
        return self.count() <= 0

    def player_join(self, secKey, playerName):
        print("player join")
        player = self.players[secKey]
        player.isPlaying = True
        player.name = playerName
        self.send_scoreboard()
        self.update_and_send_state()

    def player_leave(self, secKey):
        print("player leave")
        player = self.players[secKey]
        player.isPlaying = False
        self.send_scoreboard()
        self.update_and_send_state()

    def add_player_points(self, player):
        index = len(self.playerThatFound)
        lenPointsRepartitionMinusOne = len(Lobby.pointsRepartition) - 1
        if index >= lenPointsRepartitionMinusOne:
            index = lenPointsRepartitionMinusOne

        self.playerThatFound.append(player)
        player.add_points(Lobby.pointsRepartition[index])

    def player_submit(self, secKey, answer):
        # Can submit now...
        if Lobby.QUESTION != self.state:
            return
        player = self.players[secKey]
        if not player.can_earn_points():
            return

        # TODO : Check less restrictive
        if answer == self.currentSauce["answer"]:
            # right answer
            self.add_player_points(player)
            if len(self.playerThatFound) >= self.count_players():
                self.answer()
            self.send_scoreboard()

    def __str__(self):
        s = "--" + self.name + ", status : " + str(self.state) + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s

    def send_scoreboard(self):
        print("send scoreboard")

        # Players and spectators
        scoreboard = {}
        players = []
        spectators = []
        for player in self.players.values():
            playerStatus = player.get_status()
            if player.isPlaying:
                players.append(playerStatus)
            else:
                spectators.append(playerStatus)
        # sorted by score
        scoreboard["players"] = list(
            sorted(players, key=lambda x: -x["score"]))
        # sorted by name
        scoreboard["spectators"] = list(
            sorted(spectators, key=lambda x: x["name"]))

        # Handle history
        scoreboard["history"] = []
        for sauce, players in self.history[::-1]:
            d = {}
            d["answer"] = sauce["answer"]
            d["players"] = []
            for p in players:
                d["players"].append(p.name)
            scoreboard["history"].append(d)
        scoreboard["datetime"] = self.datetime.timestamp()
        self.broadcast(
            {"type": "scoreboard", "data": scoreboard})

    def send_waiting_for_players(self):
        print("send waiting for players")
        self.state = Lobby.WAITING_FOR_PLAYERS
        waiting_for_players = {}
        waiting_for_players["qte"] = Lobby.minPlayers - self.count_players()
        waiting_for_players["datetime"] = self.datetime.timestamp()
        self.broadcast(
            {"type": "waiting_for_players", "data": waiting_for_players})

    def send_game_starts_soon(self):
        print("send game starts soon")
        self.state = Lobby.GAME_START_SOON
        game_starts_soon = {}
        game_starts_soon["datetime"] = self.datetime.timestamp()
        self.broadcast(
            {"type": "game_starts_soon", "data": game_starts_soon})

    def send_question(self):
        print("send question")
        self.state = Lobby.QUESTION
        question = {}
        question["question"] = self.currentSauce["question"]
        question["type"] = self.currentSauce["type"]
        question["category"] = self.currentSauce["category"]
        question["datetime"] = self.datetime.timestamp()
        self.broadcast({"type": "question", "data": question})

    def send_answer(self):
        print("send answer")
        self.state = Lobby.ANSWER
        answer = {}
        answer["answer"] = self.currentSauce["answer"]
        answer["datetime"] = self.datetime.timestamp()
        data = {"type": "answer", "data": answer}
        self.broadcast(data)

    def send_game_end(self):
        print("send game end")
        self.state = Lobby.GAME_END
        game_end = {}
        game_end["datetime"] = self.datetime.timestamp()
        self.broadcast({"type": "game_end", "data": game_end})

    def broadcast(self, data):
        for player in self.players.values():
            player.socket.send(text_data=json.dumps(data))
