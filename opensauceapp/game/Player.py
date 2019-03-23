import json
from secrets import token_hex
import random
import string

class Player:

    #https://evert.meulie.net/faqwd/complete-list-anonymous-animals-on-google-drive-docs-sheets-slides/
    animals = ["Alligator", "Anteater", "Armadillo", "Auroch", "Axolotl", "Badger", "Bat", "Bear", "Beaver", "Buffalo", "Camel", "Capybara", "Chameleon", "Cheetah", "Chinchilla", "Chipmunk", "Chupacabra", "Cormorant", "Coyote", "Crow", "Dingo", "Dinosaur", "Dog", "Dolphin", "Duck", "Elephant", "Ferret", "Fox", "Frog", "Giraffe", "Gopher", "Grizzly", "Hedgehog", "Hippo", "Hyena", "Ibex", "Ifrit", "Iguana", "Jackal", "Kangaroo", "Koala", "Kraken", "Lemur", "Leopard", "Liger", "Lion", "Llama", "Loris", "Manatee", "Mink", "Monkey", "Moose", "Narwhal", "Nyan Cat", "Orangutan", "Otter", "Panda", "Penguin", "Platypus", "Pumpkin", "Python", "Quagga", "Rabbit", "Raccoon", "Rhino", "Sheep", "Shrew", "Skunk", "Squirrel", "Tiger", "Turtle", "Walrus", "Wolf", "Wolverine", "Wombat"]

    def __init__(self, socket):
        self.socket = socket
        self.id = token_hex(16)
        self.name = random.choice(Player.animals)
        self.isAdmin = False
        self.reset_game()
        self.send_player_id()

    def set_name(self, new_name):
        without_space_name = new_name.translate(str.maketrans('', '', string.whitespace))
        if(len(without_space_name) > 0):
            self.name = new_name

    def can_earn_points(self):
        return self.points_this_round <= 0

    def reset_game(self):
        self.score = 0
        self.points_this_round = 0
        self.isPlaying = False

    def reset_round(self):
        self.score += self.points_this_round
        self.points_this_round = 0

    def add_points(self, points):
        if self.can_earn_points():
            self.points_this_round = points

    def send_player_id(self):
        data = {}
        data["type"] = "welcome"
        data["data"] = self.id
        jsondumps = json.dumps(data)
        self.socket.send(text_data=jsondumps)

    def __str__(self):
        s = ""
        if self.name:
            s += self.name + " "
        if not self.isPlaying:
            s += "(spectating)"
        else:
            s += str(self.score)
        return s

    def send(self, data):
        jsondumps = json.dumps(data)
        self.socket.send(text_data=jsondumps)

    def get_status(self):
        status = {}
        status["id"] = self.id
        status["name"] = self.name
        status["isAdmin"] = self.isAdmin
        status["isPlaying"] = self.isPlaying
        status["score"] = self.score
        status["points_this_round"] = self.points_this_round
        return status
