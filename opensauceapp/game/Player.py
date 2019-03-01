class Player:
    cpt = 0
    def __init__(self, socket):
        self.socket = socket
        self.isPlaying = False
        self.isAdmin = False
        self.isOwner = False
        self.name = "Anonyme " + str(Player.cpt)
        Player.cpt += 1
        self.score = 0
        # -1 : not found yet
        self.points_this_round = None
        self.reset_round()

    def can_earn_points(self):
        return self.points_this_round < 0

    def reset_round(self):
        self.points_this_round = -1

    def add_points(self, points):
        if self.can_earn_points():
            self.points_this_round = points
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

    def get_status(self):
        status = {}
        status["name"] = self.name
        status["isAdmin"] = self.isAdmin
        status["isOwner"] = self.isOwner
        status["isPlaying"] = self.isPlaying
        status["score"] = self.score
        status["points_this_round"] = self.points_this_round
        return status
