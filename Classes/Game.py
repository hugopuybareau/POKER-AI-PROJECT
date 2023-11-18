class Game :
    def __init__(self, username : str, players_name : list, hand : list) :
        self.username = username
        self.players_name = players_name
        self.hand = hand
        self.cards = None

    #TODO
    def updatePlayers(self) :
        self.players = None

    def updateCards(self, cards : list) :
        self.cards = cards