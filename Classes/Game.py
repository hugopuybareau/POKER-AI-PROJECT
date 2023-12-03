from Players import Player, MainPlayer
from Cards import *
from Round import * 

class Game :

    def __init__(self, players_name : list, players_prize_bb : list, button_position : str) : #Je pars du principe que players_name est rangé dans le sens des aiguilles d'une montre
        
        self.main_player = None
        self.players = []
        self.button_position = button_position
        self.initPlayers(players_name, players_prize_bb)

    def updateButtonPosition (self, players_name, button_position) : 
        old_position = button_position
        self.button_position = players_name[players_name.index(old_position)+1]

    def initPlayers(self, players_name : list, players_prize_bb : list) :
        players = []
        for i in range(len(players_name)) :
            username = players_name[i]
            if username != 'me' :
                players.append(Player(username, players_prize_bb[i]))
            else :
                self.main_player = MainPlayer(username, players_prize_bb[i])
                players.append(MainPlayer(username, players_prize_bb[i]))
        
        self.players = players

    def newRound(self, main_player : MainPlayer, players : list, button_position) :
        Round(main_player, players, button_position)

    def player_alone(self) :
        count = 0
        for p in self.players :
            if p.isFolded() :
                count += 1
            
        return count == len(self.players)

if __name__ == "__main__" : 
    game = Game(['op1', 'me', 'op2', 'op3', 'op4', 'op5'], [50] * 6)


            