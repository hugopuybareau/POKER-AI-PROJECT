from Players import Player, MainPlayer
from Cards import *
from Round import *

positions = ['utg_0', 'utg_1', 'utg_2', 'utg_3', 'small_blind', 'big_blind'] 

class Game :

    def __init__(self, players_name : list, players_prize_bb : list) :
        
        self.main_player = None
        self.players = []
        self.initPlayers(players_name, players_prize_bb)
        position = []

    def initPlayers(self, players_name : list, players_prize_bb : list) :
        players = []
        for i in range(len(players_name)) :
            username = players_name[i]
            if username != 'me' :
                players.append(Player(username, positions[i], players_prize_bb[i]))
            else :
                self.main_player = MainPlayer(username, positions[i], players_prize_bb[i])
        
        self.players = players

    def newRound(self, main_player : MainPlayer, players : list) :

        Round()

    def player_alone(self) :
        count = 0
        for p in self.players :
            if p.isFolded() :
                count += 1
            
        return count == len(self.players)

if __name__ == "__main__" : 
    game = Game(['op1', 'me', 'op2', 'op3', 'op4', 'op5'], [50] * 6)

print(game.main_player.username)


            