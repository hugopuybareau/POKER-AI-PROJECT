from Players import Player, MainPlayer
from Cards import *

deals = ['pre_flop', 'flop', 'turn', 'river']
decisions = ['fold', 'check_fold', 'check', 'call', '3_BB', '2_raise', '50%pot', 'pot' 'all_in']
positions = ['utg_0', 'utg_1', 'utg_2', 'utg_3', 'small_blind', 'big_blind'] 

class Round :

    def __init__(self, main_player : MainPlayer, players : list, hand : Hand, pot_bb : float, to_call_bb : float, stage=0, button = 'utg_3') :
        self.pot_bb = pot_bb
        self.decision = []
        self.hand = hand
        self.players = players
        self.to_call_bb = to_call_bb 

    def updateCards(self, cards : list) :
        self.cards = cards

    def updatePotBB(self, pot_bb : float) : 
        self.pot_bb = pot_bb

    def updateStage(self, stage) :
        self.stage += 1

    def updateDecision(self, table : Table, hand : Hand, pot_bb) : 
        if self.stage == 0 : 
            playable_hands = []
            if (self.main_player.position == positions[0]) or (self.main_player.position == positions[1]) or (self.main_player.position == positions[2]):  #UTG0 ou UTG1 ou UTG2, On raise sur une petite range 
                for key, values in storage_preflop.items() : 
                    if values[len(self.players)-2]/100 > 0.2 : 
                        playable_hands.append(key) 
                        for i in playable_hands : 
                            if str(hand) == i : 
                                if pot_bb == 1.5 :  #First to raise
                                    self.decision.append(decisions[4])
                                if pot_bb > 7.5 :  #Y'a un pelo qui s'excite go le laisser jouer tout seul
                                    self.decision.append(decisions[0])

            if (self.main_player.position == positions[3]) or (self.main_player.position == positions[4]) and pot_bb == 1.5: #UTG3 ou SB, On a une range plus large si personne a raise
                playable_hands = []
                for key, values in storage_preflop.items() : 
                    if values[len(self.players)-2]/100 > 0.3 : #On prend plus large parce que personne nous a raise donc plus simple pour voler les blinds
                        playable_hands.append(key) 
                        for i in playable_hands : 
                            if str(hand) == i : 
                                self.decision.append(decisions[4])
            
            if (self.main_player.position == positions[5]) or (self.main_player.position == positions[4]) or (self.main_player.position == positions[3]) :  
                playable_hands = []
                for key, values in storage_preflop.items() : 
                        if values[len(self.players)-2]/100 > 0.15 : #On prend plus tight parce qu'on va parler avant le mec qui nous a raise pour toute la suite de la partie 
                            playable_hands.append(key) 
                            for i in playable_hands : 
                                if str(hand) == i :
                                    if self.main_player.diff_to_call < 5 : 
                                        self.decision.append(decisions[5]) 
                                    else : 
                                        self.decision.append(decisions[0])

            if self.decisions != [] : #Cas de re-raise par un adversaire
                if (self.main_player.diff_to_call > 6) or ((self.main_player.diff_to_call < 5) and pot_bb > 15): 
                    self.decisions[0] = decisions[0]
                if  self.main_player.diff_to_call <= 6 :
                    self.decisions[0] = decisions[3] 