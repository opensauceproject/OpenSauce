import random
import datetime
from threading import Thread
from time import sleep
import json
import string
from secrets import token_hex
from asgiref.sync import async_to_sync

from ..models import Sauce
from ..models import SauceCategory
from .Tools import sanitize, str_delta

from .Player import Player


class Lobby:
    # States
    WAITING_FOR_PLAYERS = 0
    GAME_START_SOON = 1
    QUESTION = 2
    ANSWER = 3
    GAME_END = 4

    timeout_when_state_game_start_soon = datetime.timedelta(seconds=1)
    timeout_when_question = datetime.timedelta(seconds=4)
    timeout_when_answer = datetime.timedelta(seconds=4)
    timeout_when_game_end = datetime.timedelta(seconds=3)

    score_goals = [10, 20, 30, 50, 100, 200]
    default_score_goal = 20

    ignored_prefix = ["the", "a", "an", "le", "la", "les"]
    answer_max_delta = 1

    min_players = 3
    max_round_without_points = 10

    # the last is repeated for all the next players
    points_repartition = [5, 3, 2, 1]

    def __init__(self, name):
        self.name = name
        self.players = {}
        self.set_default_settings()
        self.goto_waiting_for_players()

    def set_default_settings(self):
        """Everything is enabled by default"""
        settings = {}
        settings["categories"] = []
        settings["score_goal_value"] = Lobby.default_score_goal
        categories = SauceCategory.objects.all()
        for category in categories:
            for difficulty in range(1, 4):  # 1-3
                setting = {'category_id': category.id,
                           'difficulty': difficulty, 'value': True}
                settings["categories"].append(setting)
        self.settings = settings

    def fetch_sauces_from_settings(self):
        all_sauces = Sauce.objects.all()
        filtred_sauces = []

        settings_lookup = {}
        # print(self.settings)
        for category in self.settings["categories"]:
            category_id = category["category_id"]
            difficulty = category["difficulty"]
            value = category["value"]
            settings_lookup[(category_id, difficulty)] = value

        # it's difficult with filter so we do it manualy
        for sauce in all_sauces:
            if settings_lookup[(sauce.sauce_category.id, sauce.difficulty)]:
                filtred_sauces.append(sauce)

        return filtred_sauces

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

    def get_best_player(self):
        playerSorted = sorted(self.get_players(), key=lambda p: p.score)
        if len(playerSorted) <= 0:
            return False
        else:
            return playerSorted[0]

    def get_current_state(self, complete_state = False):
        if Lobby.WAITING_FOR_PLAYERS == self.state:
            return self.get_waiting_for_players()
        elif Lobby.GAME_START_SOON == self.state:
            return self.get_game_starts_soon()
        elif self.state == Lobby.QUESTION:
            return self.get_question()
        elif Lobby.ANSWER == self.state:
            return self.get_answer()
        elif Lobby.GAME_END == self.state:
            return self.get_game_end()
        else:
            raise "Unhandled state"

#  ____       _
# |  _ \  ___| | __ _ _   _
# | | | |/ _ \ |/ _` | | | |
# | |_| |  __/ | (_| | |_| |
# |____/ \___|_|\__,_|\__, |
#                     |___/

    def delay_game_start_soon(self):
        self.datetime = datetime.datetime.now() + Lobby.timeout_when_state_game_start_soon
        sleep(Lobby.timeout_when_state_game_start_soon.total_seconds())
        if Lobby.GAME_START_SOON == self.state:
            self.goto_question_state(True)

    def delay_question(self, state_id):
        self.datetime = datetime.datetime.now() + Lobby.timeout_when_question
        sleep(Lobby.timeout_when_question.total_seconds())
        # Verify that this the correct state to give the answer
        if Lobby.QUESTION == self.state and state_id == self.state_id:
            self.goto_answer_state()
            self.round_without_points += 1
            if self.round_without_points >= Lobby.max_round_without_points:
                self.reset()

    def delay_answer(self):
        self.datetime = datetime.datetime.now() + Lobby.timeout_when_answer
        sleep(Lobby.timeout_when_answer.total_seconds())
        if Lobby.ANSWER == self.state:
            best_player = self.get_best_player()
            if best_player and best_player.score + best_player.points_this_round >= self.settings["score_goal_value"]:
                self.goto_game_end_state()
            else:
                self.goto_question_state()

    def delay_game_end(self):
        self.datetime = datetime.datetime.now() + Lobby.timeout_when_game_end
        sleep(Lobby.timeout_when_game_end.total_seconds())
        self.goto_waiting_for_players()


#   ____       _          ____  _        _
#  / ___| ___ | |_ ___   / ___|| |_ __ _| |_ ___
# | |  _ / _ \| __/ _ \  \___ \| __/ _` | __/ _ \
# | |_| | (_) | || (_) |  ___) | || (_| | ||  __/
#  \____|\___/ \__\___/  |____/ \__\__,_|\__\___|

    def goto_waiting_for_players(self):
        self.state = Lobby.WAITING_FOR_PLAYERS
        self.round_without_points = 0
        self.current_sauce = None
        self.state_id = token_hex(16)
        self.datetime = datetime.datetime.now()
        self.player_that_found = []
        for player in self.players.values():
            player.reset_game()
        self.history = []
        self.sauces = self.fetch_sauces_from_settings()
        self.broadcast(self.get_scoreboard())
        self.broadcast(self.get_current_state())

    def goto_question_state(self, first_round=False):
        self.state = Lobby.QUESTION

        # Reset previous round
        for player in self.players.values():
            player.reset_round()
        self.player_that_found = []

        # Broadcast the scoreboard when it's useful
        if not first_round:
            self.broadcast(self.get_scoreboard())

        # Set new sauce
        self.current_sauce = random.choice(self.sauces)
        # Set a new state id, used for delayed thread
        self.state_id = token_hex(16)
        # Set the end time

        # Run a thread to give the answer after a delay
        Thread(target=self.delay_question, args=(self.state_id,)).start()

        self.broadcast(self.get_current_state())

    def goto_answer_state(self):
        self.state = Lobby.ANSWER

        # Add the current sauce to the history with the players
        self.history.append((self.current_sauce, self.player_that_found))

        # Run a thread to continue after giving the answer
        Thread(target=self.delay_answer).start()
        self.broadcast(self.get_answer())

    def goto_game_start_soon_state(self):
        self.state = Lobby.GAME_START_SOON
        Thread(target=self.delay_game_start_soon).start()
        self.broadcast(self.get_current_state())

    def goto_game_end_state(self):
        self.state = Lobby.GAME_END
        Thread(target=self.delay_game_end).start()
        self.broadcast(self.get_current_state())

#  ____  _
# |  _ \| | __ _ _   _  ___ _ __
# | |_) | |/ _` | | | |/ _ \ '__|
# |  __/| | (_| | |_| |  __/ |
# |_|   |_|\__,_|\__, |\___|_|
#                |___/
#  __  __                                     _
# |  \/  | _____   _____ _ __ ___   ___ _ __ | |_ ___
# | |\/| |/ _ \ \ / / _ \ '_ ` _ \ / _ \ '_ \| __/ __|
# | |  | | (_) \ V /  __/ | | | | |  __/ | | | |_\__ \
# |_|  |_|\___/ \_/ \___|_| |_| |_|\___|_| |_|\__|___/

    def player_add(self, secKey, socket):
        player = Player(socket)
        if len(self.players) < 1:
            player.isOwner = True
        self.players[secKey] = player
        player.send(self.get_current_state())
        player.send(self.get_settings())
        self.broadcast(self.get_scoreboard())

    def player_remove(self, secKey):
        if secKey in self.players:
            del self.players[secKey]
        self.broadcast(self.get_scoreboard())
        # if the last player is remove the lobby tell to remove the lobby
        return self.count() <= 0

    def player_join(self, secKey, playerName):
        player = self.players[secKey]
        player.isPlaying = True
        player.set_name(playerName)
        if Lobby.WAITING_FOR_PLAYERS == self.state:
            if self.count_players() >= Lobby.min_players:
                self.goto_game_start_soon_state()
        self.broadcast(self.get_scoreboard())

    def player_leave(self, secKey):
        player = self.players[secKey]
        player.reset_game()
        if self.count_players() <= 0:
            self.reset()
        else:
            self.broadcast(self.get_scoreboard())

#  ____  _                         __  __
# |  _ \| | __ _ _   _  ___ _ __  |  \/  | ___  ___ ___  __ _  __ _  ___  ___
# | |_) | |/ _` | | | |/ _ \ '__| | |\/| |/ _ \/ __/ __|/ _` |/ _` |/ _ \/ __|
# |  __/| | (_| | |_| |  __/ |    | |  | |  __/\__ \__ \ (_| | (_| |  __/\__ \
# |_|   |_|\__,_|\__, |\___|_|    |_|  |_|\___||___/___/\__,_|\__, |\___||___/
#                |___/                                        |___/

    def get_current_points(self):
        index = len(self.player_that_found)
        len_points_repartition_MinusOne = len(Lobby.points_repartition) - 1
        if index >= len_points_repartition_MinusOne:
            index = len_points_repartition_MinusOne
        return Lobby.points_repartition[index]

    def player_submit(self, secKey, submited_answer):
        player = self.players[secKey]
        # Can you submit now ?
        if Lobby.QUESTION != self.state:
            return
        if not player.isPlaying:
            return
        if not player.can_earn_points():
            return

        current_answer = self.current_sauce.answer

        submited_answer_s = sanitize(submited_answer, Lobby.ignored_prefix)
        real_answer_s = sanitize(current_answer, Lobby.ignored_prefix)

        delta = str_delta(submited_answer_s, real_answer_s)

        if delta <= Lobby.answer_max_delta:
            # correct answer
            self.round_without_points = 0

            player.add_points(self.get_current_points())
            self.player_that_found.append(player)

            if len(self.player_that_found) >= self.count_players():
                # go to the answer state
                self.goto_answer_state()
            self.broadcast(self.get_scoreboard())

    def player_set_settings(self, settings):
        self.settings = settings
        self.sauces = self.fetch_sauces_from_settings()
        # for i in self.sauces:
        #     print(i)
        self.broadcast(self.get_settings())

#  ____  _        _                  _ ____   ___  _   _
# / ___|| |_ __ _| |_ ___  ___      | / ___| / _ \| \ | |
# \___ \| __/ _` | __/ _ \/ __|  _  | \___ \| | | |  \| |
#  ___) | || (_| | ||  __/\__ \ | |_| |___) | |_| | |\  |
# |____/ \__\__,_|\__\___||___/  \___/|____/ \___/|_| \_|

    def get_settings(self):
        settings = {}
        settings["settings"] = self.settings
        settings["datetime"] = self.datetime.timestamp()
        return {"type": "settings", "data": settings}

    def get_scoreboard(self):
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
            if sauce is None:
                continue
            d = {}
            d["id"] = sauce.id
            d["answer"] = sauce.answer
            d["players"] = []
            for p in players_history:
                d["players"].append(p.name)
            scoreboard["history"].append(d)

        scoreboard["datetime"] = self.datetime.timestamp()
        return {"type": "scoreboard", "data": scoreboard}

    def get_waiting_for_players(self):
        waiting_for_players = {}
        waiting_for_players["qte"] = Lobby.min_players - self.count_players()
        return {"type": "waiting_for_players", "data": waiting_for_players}

    def get_game_starts_soon(self):
        game_starts_soon = {}
        game_starts_soon["datetime"] = self.datetime.timestamp()
        return {"type": "game_starts_soon", "data": game_starts_soon}

    def get_question(self):
        question = {}
        question["question"] = self.current_sauce.question
        question["media_type"] = self.current_sauce.media_type
        question["category"] = self.current_sauce.sauce_category.name
        question["datetime"] = self.datetime.timestamp()
        return {"type": "question", "data": question}

    def get_answer(self):
        answer = {}
        answer["answer"] = self.current_sauce.answer
        answer["question"] = self.current_sauce.question
        answer["media_type"] = self.current_sauce.media_type
        answer["category"] = self.current_sauce.sauce_category.name
        return {"type": "answer", "data": answer}

    def get_game_end(self):
        game_end = {}
        game_end["winner"] = self.get_best_player().name
        return {"type": "game_end", "data": game_end}

#  __  __ _
# |  \/  (_)___  ___
# | |\/| | / __|/ __|
# | |  | | \__ \ (__
# |_|  |_|_|___/\___|

    def broadcast(self, data):
        jsondumps = json.dumps(data)
        for player in self.players.values():
            player.socket.send(text_data=jsondumps)

    def __str__(self):
        s = "--" + self.name + ", status : " + str(self.state) + "\n"
        for name, player in self.players.items():
            s += "---- " + str(name) + " : " + str(player) + "\n"
        return s
