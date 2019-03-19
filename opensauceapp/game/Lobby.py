from .Player import Player

import random
import datetime
from threading import Thread
from time import sleep
import json
import string
import unidecode
from asgiref.sync import async_to_sync

from ..models import Sauce


# TODO :
# - fix send when player join/leave/add/remove
# -

class Lobby:
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

    score_goals = [10, 20, 30, 50, 100, 200]
    default_score_goal = 50

    ignored_prefix_char_sequence = ["the", "a", "an", "le", "la", "les"]

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
        self.sauces = Sauce.objects.all()

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

    def set_settings(self, settings):
        self.settings = settings

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
        self.currentSauce = random.choice(self.sauces)
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
        if not player.isPlaying:
            return
        if not player.can_earn_points():
            return

        print(Lobby.sanitize(answer), Lobby.sanitize(self.currentSauce.answer))
        if Lobby.sanitize(answer) == Lobby.sanitize(self.currentSauce.answer):
            # correct answer
            self.add_player_points(player)
            if len(self.playerThatFound) >= self.count_players():
                self.answer()
            self.send_scoreboard()

    @staticmethod
    def sanitize(s):
        # any special char unicode char to the closest ascci char
        s = unidecode.unidecode(s)
        # remove punctuation and remove whitespaces
        s = s.translate(str.maketrans('', '', string.punctuation))
        # only lower cases
        s = s.lower()
        # remove special char sequence
        for sequence in Lobby.ignored_prefix_char_sequence:
            l = len(sequence)
            word_prefix = s[:l]
            if word_prefix == sequence:
                s = s[l:]
                break
        s = s.translate(str.maketrans('', '', string.whitespace))
        return s

    def __str__(self):
        s = "--" + self.name + ", status : " + str(self.state) + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s

    def send_scoreboard(self):
        # Players and spectators
        players = []
        spectators = []
        for player in self.players.values():
            player_status = player.get_status()
            if player.isPlaying:
                players.append(player_status)
            else:
                spectators.append(player_status)

        scoreboard = {}
        # sorted by score
        scoreboard["players"] = list(
            sorted(players, key=lambda x: -x["score"]))
        # sorted by name
        scoreboard["spectators"] = list(
            sorted(spectators, key=lambda x: x["name"]))

        # Handle history
        scoreboard["history"] = []
        for sauce, players_history in self.history[::-1]:
            d = {}
            d["id"] = sauce.id
            d["answer"] = sauce.answer
            d["players"] = []
            for p in players_history:
                d["players"].append(p.name)
            scoreboard["history"].append(d)

        scoreboard["datetime"] = self.datetime.timestamp()

        # print("send scoreboard", scoreboard)
        data = {"type": "scoreboard", "data": scoreboard}
        self.broadcast(data)

    def send_waiting_for_players(self):
        self.state = Lobby.WAITING_FOR_PLAYERS
        waiting_for_players = {}
        waiting_for_players["qte"] = Lobby.minPlayers - self.count_players()
        waiting_for_players["datetime"] = self.datetime.timestamp()
        # print("send waiting for players : ", waiting_for_players)
        self.broadcast(
            {"type": "waiting_for_players", "data": waiting_for_players})

    def send_game_starts_soon(self):
        self.state = Lobby.GAME_START_SOON
        game_starts_soon = {}
        game_starts_soon["datetime"] = self.datetime.timestamp()
        # print("send game starts soon : ", game_starts_soon)
        self.broadcast(
            {"type": "game_starts_soon", "data": game_starts_soon})

    def send_question(self):
        self.state = Lobby.QUESTION
        question = {}
        question["question"] = self.currentSauce.question
        question["media_type"] = self.currentSauce.media_type
        question["category"] = self.currentSauce.sauce_category.name
        question["datetime"] = self.datetime.timestamp()
        # print("send question : ", question)
        self.broadcast({"type": "question", "data": question})

    def send_answer(self):
        self.state = Lobby.ANSWER
        answer = {}
        answer["answer"] = self.currentSauce.answer
        answer["datetime"] = self.datetime.timestamp()
        # print("send answer : ", answer)
        data = {"type": "answer", "data": answer}
        self.broadcast(data)

    def send_game_end(self):
        self.state = Lobby.GAME_END
        game_end = {}
        game_end["datetime"] = self.datetime.timestamp()

        # print("send game end : ", game_end)
        self.broadcast({"type": "game_end", "data": game_end})

    def broadcast(self, data):
        for player in self.players.values():
            player.socket.send(text_data=json.dumps(data))
