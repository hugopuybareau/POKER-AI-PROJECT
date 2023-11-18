class Game :
    def __init__(self, username : str, players_name : list, hand : list, prize_bb : float, pot_bb = float) :
        self.username = username
        self.players_name = players_name
        self.hand = hand
        self.cards = [None] * 5

    #TODO
    def updatePlayers(self) :
        self.players = None

    def updateCards(self, cards : list) :
        self.cards = cards