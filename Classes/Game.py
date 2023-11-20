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

    deals = ['pre_flop', 'flop', 'turn', 'river']
    decisions = ['fold', 'check_fold', 'check', 'call', '2_bet', '3_bet', '2_raise', '3_raise' 'all_in']
    positions = ['small_blind', 'big_blind', 'utg_0', 'utg_1', 'utg_2', 'utg_3']

<<<<<<< Updated upstream
    def __init__(self, main_player : MainPlayer, players : list, hand : Hand, button = 'utg_3', pot_bb : float, to_call_bb : float stage=0) :
=======
    def __init__(self, main_player : MainPlayer, players : list, hand : Hand, button : int, pot_bb : float, stage=0) :
        self.button = button
>>>>>>> Stashed changes
        self.pot_bb = pot_bb
        self.decision = []
        self.hand = hand
        self.players = players
        self.decision_rate = decision_rates[len(players)]
        self.to_call_bb = to_call_bb 

    def updateCards(self, cards : list) :
        self.cards = cards

    def updatePotBB(self, pot_bb : float) : 
        self.pot_bb = pot_bb

    def updateStage(self, stage) :
        self.stage += 1

    def updateDecision(self, table : Table, hand : Hand, pot_bb) : 
        if self.stage == 0 : 
            for key, values in stats_preflop.items() : 
                if values[len(players)-2]/100 > decision_rate : 
                    playable_hands.append(key) 
                    for i in playable_hands : 
                        if str(hand) == i : 

                            if (self.main_player.position != positions[2]) : #SB or BB or #UNDER THE GUN+1/+2/+3/+4 Je mets la même pour l'instant mais en sah c'est pas vraiment pareil faut que je refasse des recherches je me souviens plus 
                                if (pot_bb > 4) and (diff_to_call < 3): #POT ALREADY CALLED/SMALL RAISED, 2RAISE CONTROL
                                    self.decision.append(decisions[6])
                                if (pot_bb > 4) and (diff_to_call < 6): #POT ALREADY RAISED, WE CALL
                                    self.decision.append(decisions[3])
                                if diff_to_call > 10 : #RECREATIONAL PLAYER WE FOLD 
                                    self.decision.append(decision[0])
                                if 1.5 < pot_bb < 4 : #POT ONLY CALLED, WE TAKE CONTROL / STEAL THE BLINDS W 3RAISE
                                    self.decision.append(decisions[7])

                            if self.main_player.position == positions[2] : #UNDER THE GUN, WE TAKE CONTROL
                                self.decision.append(decisions[5])

                        else : 
                            if (self.main_player.position == positions[1]) and (self.main_player.diff_to_call == 0): 
                                self.decision.append(decisions[2])
        if self.stage == 1 : 

            





    
    
            
            
                

    

    