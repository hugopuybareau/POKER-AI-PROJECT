from Players import Player, MainPlayer
from Cards import *

decision_rates = [0.5 , 0.5 , 0.5 , 0.2, 0.15, 0, 0] 

class Game :

    def __init__(self, username : str, players_name : list, players_prize_bb : list) :
        
        self.username = username

        self.main_player = None
        self.players = []
        
        self.initPlayers(players_name, players_prize_bb)

        self.decision_rate = decision_rates[len(players_name)]

    def initPlayers(self, players_name : list, players_prize_bb : list) :
        players = []
        for i in range(len(players_name)) :
            username = players_name[i]
            if i != self.position :
                players.append(Player(username, i, players_prize_bb[i]))
            else :
                self.main_player = MainPlayer(username, i, players_prize_bb[i])
        
        self.players = players

    def player_alone(self) :
        count = 0
        for p in self.players :
            if p.isFolded() :
                count += 1
            
        return count == len(self.players)
    
class Round :

    stage = {0 : 'pre_flop_bet', 1 : 'flop_bet', 2 : 'turn_bet', 3 : 'river_bet'}
    decisions = {0 : 'check_flop', 1 : 'check', 2 : 'call', 3 :'2_bet', 4 : '3_bet', 5 : 'all_in'}
    positions =  {0: 'small_blind', 1 : 'big_blind', 2 : 'utg_0', 3 : 'utg_1', 4 : 'utg_2', 5 : 'utg_3', 6 : 'utg_4', 7 : 'utg_5'}

    def __init__(self, main_player : MainPlayer, players : list, hand : Hand, button : int, pot_bb : float, stage=0) :
        self.pot_bb = pot_bb
        self.decision = []
        self.cards = []
        self.players = []
        self.decision_rate = decision_rates[len(players)]

    def updateCards(self, cards : list) :
        self.cards = cards

    def updatePotBB(self, pot_bb : float) : 
        self.pot_bb = pot_bb
    
    def updateDecision(self, stage, decisions, table : Table, hand : Hand, pot_bb) : 
        if stage == 0 : 
            if self.main_player.position == 0 :
                if pot_bb > 4 :
                    self.decision.append(decisions[2])





    
    
            
            
                

    

    