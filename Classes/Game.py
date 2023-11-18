class Game :
    def __init__(self, username : str, players_name : list, hand : list, prize_bb : float, pot_bb = float) :
        self.username = username
        self.players_name = players_name
        self.hand = hand
<<<<<<< Updated upstream
        self.cards = [None] * 5
=======
        self.cards = None
        self.prize_bb = None
        self.pot_bb = None
        

        
>>>>>>> Stashed changes

    #TODO
    def updatePlayers(self) :
        self.players = None

    def updateCards(self, cards : list) :
        self.cards = cards