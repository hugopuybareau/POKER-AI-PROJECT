from Players import Player, MainPlayer
from Cards import *
from Round import * 

class Game :

    def __init__(self, players_name : list, players_prize_bb : list, button_position : str) : #Je pars du principe que players_name est rangé dans le sens des aiguilles d'une montre
        
        self.main_player = None
        self.players = []
        self.button_position = button_position
        self.initPlayers(players_name, players_prize_bb)
        self.players_name = players_name

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

    def newRound(self, main_player : MainPlayer, players_name, players, button_position) :
        round = Round(main_player, players, players_name, button_position)
        old_position = button_position
        self.button_position = players_name[players_name.index(old_position)+1]


if __name__ == "__main__" : 
    game = Game(['op1', 'me', 'op2', 'op3', 'op4', 'op5'], [50] * 6, 'me')
    print(game.button_position)
    game.newRound(game.main_player, game.players_name, game.players, game.button_position)
    for p in game.players : 
        print(p.position)
    game.newRound(game.main_player, game.players_name, game.players, game.button_position)
    for p in game.players : 
        print(p.position)


            