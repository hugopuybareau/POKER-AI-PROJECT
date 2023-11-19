class Player :

    def __init__(self, username : str, position : int, prize_bb : float) :
        self.username = username
        self.position = position
        self.prize_bb = prize_bb
        self.all_in = 0
        self.three_bet = 0
        self.bet_bb = 0
        self.folded = False

    def updateBetBB(self, bet_bb : float) :
        self.bet_bb = bet_bb

    def updatePrizeBB(self, prize_bb : float) :
        self.prize_bb = prize_bb

    def fold(self) :
        self.folded = True

    def isFolded(self) :
        return self.folded

class MainPlayer(Player) :

    def __init__(self, username : str, position : int, prize_bb : float) :
        Player.__init__(self, username, position, bet_bb, prize_bb)
        self.hand = hand