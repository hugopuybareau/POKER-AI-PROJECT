from itertools import combinations
import random as rd
import time

preflop_stats = {
    "A-A":[85.3,73.4,63.9,55.9,49.2,43.6,38.8,34.7,31.1],
    "A-Ks":[67.0,50.7,41.4,35.4,31.1,27.7,25.0,22.7,20.7],
    "A-K":[65.4,48.2,38.6,32.4,27.9,24.4,21.6,19.2,17.2],
    "A-Qs":[66.1,49.4,39.9,33.7,29.4,26.0,23.3,21.1,19.3],
    "A-Q":[64.5,46.8,36.9,30.4,25.9,22.5,19.7,17.5,15.5],
    "A-Js":[65.4,48.2,38.5,32.2,27.8,24.5,22.0,19.9,18.1],
    "A-J":[63.6,45.6,35.4,28.9,24.4,21.0,18.3,16.1,14.3],
    "A-10s":[64.7,47.1,37.2,31.0,26.7,23.5,21.0,18.9,17.3],
    "A-10":[62.9,44.4,34.1,27.6,23.1,19.8,17.2,15.1,13.4],
    "A-9s":[63.0,44.8,34.6,28.4,24.2,21.1,18.8,16.9,15.4],
    "A-9":[60.9,41.8,31.2,24.7,20.3,17.1,14.7,12.8,11.2],
    "A-8s":[62.1,43.7,33.6,27.4,23.3,20.3,18.0,16.2,14.8],
    "A-8":[60.1,40.8,30.1,23.7,19.4,16.2,13.9,12.0,10.6],
    "A-7s":[61.1,42.6,32.6,26.5,22.5,19.6,17.4,15.7,14.3],
    "A-7":[59.1,39.4,28.9,22.6,18.4,15.4,13.2,11.4,10.1],
    "A-6s":[60.0,41.3,31.4,25.6,21.7,19.0,16.9,15.3,14.0],
    "A-6":[57.8,38.0,27.6,21.5,17.5,14.7,12.6,10.9,9.6],
    "A-5s":[59.9,41.4,31.8,26.0,22.2,19.6,17.5,15.9,14.5],
    "A-5":[57.7,38.2,27.9,22.0,18.0,15.2,13.1,11.5,10.1],
    "A-4s":[58.9,40.4,30.9,25.3,21.6,19.0,17.0,15.5,14.2],
    "A-4":[56.4,36.9,26.9,21.1,17.3,14.7,12.6,11.0,9.8],
    "A-3s":[58.0,39.4,30.0,24.6,21.0,18.5,16.6,15.1,13.9],
    "A-3":[55.6,35.9,26.1,20.4,16.7,14.2,12.2,10.7,9.5],
    "A-2s":[57.0,38.5,29.2,23.9,20.4,18.0,16.1,14.6,13.4],
    "A-2":[54.6,35.0,25.2,19.6,16.1,13.6,11.7,10.2,9.1],
    "K-K":[82.4,68.9,58.2,49.8,43.0,37.5,32.9,29.2,26.1],
    "K-Qs":[63.4,47.1,38.2,32.5,28.3,25.1,22.5,20.4,18.6],
    "K-Q":[61.4,44.4,35.2,29.3,25.1,21.8,19.1,16.9,15.1],
    "K-Js":[62.6,45.9,36.8,31.1,26.9,23.8,21.3,19.3,17.6],
    "K-J":[60.6,43.1,33.6,27.6,23.5,20.2,17.7,15.6,13.9],
    "K-10s":[61.9,44.9,35.7,29.9,25.8,22.8,20.4,18.5,16.9],
    "K-10":[59.9,42.0,32.5,26.5,22.3,19.2,16.7,14.7,13.1],
    "K-9s":[60.0,42.4,32.9,27.2,23.2,20.3,18.1,16.3,14.8],
    "K-9":[58.0,39.5,29.6,23.6,19.5,16.5,14.1,12.3,10.8],
    "K-8s":[58.5,40.2,30.8,25.1,21.3,18.6,16.5,14.8,13.5],
    "K-8":[56.3,37.2,27.3,21.4,17.4,14.6,12.5,10.8,9.4],
    "K-7s":[57.8,39.4,30.1,24.5,20.8,18.1,16.0,14.5,13.2],
    "K-7":[55.4,36.1,26.3,20.5,16.7,13.9,11.8,10.2,9.0],
    "K-6s":[56.8,38.4,29.1,23.7,20.1,17.5,15.6,14.0,12.8],
    "K-6":[54.3,35.0,25.3,19.7,16.0,13.3,11.3,9.8,8.6],
    "K-5s":[55.8,37.4,28.2,23.0,19.5,17.0,15.2,13.7,12.5],
    "K-5":[53.3,34.0,24.5,19.0,15.4,12.9,11.0,9.5,8.3],
    "K-4s":[54.7,36.4,27.4,22.3,19.0,16.6,14.8,13.4,12.3],
    "K-4":[52.1,32.8,23.4,18.1,14.7,12.3,10.5,9.1,8.0],
    "K-3s":[53.8,35.5,26.7,21.7,18.4,16.2,14.5,13.1,12.1],
    "K-3":[51.2,31.9,22.7,17.6,14.2,11.9,10.2,8.9,7.8],
    "K-2s":[52.9,34.6,26.0,21.2,18.1,15.9,14.3,13.0,11.9],
    "K-2":[50.2,30.9,21.8,16.9,13.7,11.5,9.8,8.6,7.6],
    "Q-Q":[79.9,64.9,53.5,44.7,37.9,32.5,28.3,24.9,22.2],
    "Q-Js":[60.3,44.1,35.6,30.1,26.1,23.0,20.7,18.7,17.1],
    "Q-J":[58.2,41.4,32.6,26.9,22.9,19.8,17.3,15.3,13.7],
    "Q-10s":[59.5,43.1,34.6,29.1,25.2,22.3,19.9,18.1,16.6],
    "Q-10":[57.4,40.2,31.3,25.7,21.6,18.6,16.3,14.4,12.9],
    "Q-9s":[57.9,40.7,31.9,26.4,22.5,19.7,17.6,15.9,14.5],
    "Q-9":[55.5,37.6,28.5,22.9,19.0,16.1,13.8,12.1,10.7],
    "Q-8s":[56.2,38.6,29.7,24.4,20.7,18.0,16.0,14.4,13.2],
    "Q-8":[53.8,35.4,26.2,20.6,16.9,14.1,12.1,10.5,9.2],
    "Q-7s":[54.5,36.7,27.9,22.7,19.2,16.7,14.8,13.3,12.1],
    "Q-7":[51.9,33.2,24.0,18.6,15.1,12.5,10.6,9.2,8.0],
    "Q-6s":[53.8,35.8,27.1,21.9,18.5,16.1,14.3,12.9,11.7],
    "Q-6":[51.1,32.3,23.2,17.9,14.4,12.0,10.1,8.8,7.6],
    "Q-5s":[52.9,34.9,26.3,21.4,18.1,15.8,14.1,12.7,11.6],
    "Q-5":[50.2,31.3,22.3,17.3,13.9,11.6,9.8,8.5,7.4],
    "Q-4s":[51.7,33.9,25.5,20.7,17.6,15.4,13.7,12.4,11.3],
    "Q-4":[49.0,30.2,21.4,16.4,13.3,11.0,9.4,8.1,7.1],
    "Q-3s":[50.7,33.0,24.7,20.1,17.0,14.9,13.3,12.1,11.1],
    "Q-3":[47.9,29.2,20.7,15.9,12.8,10.7,9.1,7.9,6.9],
    "Q-2s":[49.9,32.2,24.0,19.5,16.6,14.6,13.1,11.9,10.9],
    "Q-2":[47.0,28.4,19.9,15.3,12.3,10.3,8.8,7.7,6.8],
    "J-J":[77.5,61.2,49.2,40.3,33.6,28.5,24.6,21.6,19.3],
    "J-10s":[57.5,41.9,33.8,28.5,24.7,21.9,19.7,17.9,16.5],
    "J-10":[55.4,39.0,30.7,25.3,21.5,18.6,16.3,14.5,13.1],
    "J-9s":[55.8,39.6,31.3,26.1,22.4,19.7,17.6,15.9,14.6],
    "J-9":[53.4,36.5,27.9,22.5,18.7,15.9,13.8,12.1,10.8],
    "J-8s":[54.2,37.5,29.1,24.0,20.5,17.9,15.9,14.4,13.2],
    "J-8":[51.7,34.2,25.6,20.4,16.8,14.1,12.2,10.7,9.5],
    "J-7s":[52.4,35.4,27.1,22.2,18.9,16.4,14.6,13.2,12.0],
    "J-7":[49.9,32.1,23.5,18.3,14.9,12.4,10.6,9.2,8.1],
    "J-6s":[50.8,33.6,25.4,20.6,17.4,15.2,13.5,12.1,11.1],
    "J-6":[47.9,29.8,21.4,16.5,13.2,11.0,9.3,8.0,7.0],
    "J-5s":[50.0,32.8,24.7,20.0,17.0,14.7,13.1,11.8,10.8],
    "J-5":[47.1,29.1,20.7,15.9,12.8,10.6,8.9,7.7,6.7],
    "J-4s":[49.0,31.8,24.0,19.4,16.4,14.3,12.8,11.5,10.6],
    "J-4":[46.1,28.1,19.9,15.3,12.3,10.2,8.6,7.5,6.5],
    "J-3s":[47.9,30.9,23.2,18.8,16.0,14.0,12.5,11.3,10.4],
    "J-3":[45.0,27.1,19.1,14.6,11.7,9.8,8.3,7.2,6.3],
    "J-2s":[47.1,30.1,22.6,18.3,15.6,13.7,12.2,11.1,10.2],
    "J-2":[44.0,26.2,18.4,14.1,11.3,9.4,8.0,7.0,6.2],
    "10-10":[75.1,57.7,45.2,36.4,30.0,25.3,21.8,19.2,17.2],
    "10-9s":[54.3,38.9,31.0,26.0,22.5,19.8,17.8,16.2,14.9],
    "10-9":[51.7,35.7,27.7,22.5,18.9,16.2,14.1,12.6,11.3],
    "10-8s":[52.6,36.9,29.0,24.0,20.6,18.1,16.2,14.8,13.6],
    "10-8":[50.0,33.6,25.4,20.4,16.9,14.4,12.5,11.0,9.9],
    "10-7s":[51.0,34.9,27.0,22.2,19.0,16.6,14.8,13.5,12.4],
    "10-7":[48.2,31.4,23.4,18.4,15.1,12.8,11.0,9.7,8.6],
    "10-6s":[49.2,32.8,25.1,20.5,17.4,15.2,13.6,12.3,11.2],
    "10-6":[46.3,29.2,21.2,16.5,13.4,11.2,9.5,8.3,7.3],
    "10-5s":[47.2,30.8,23.3,18.9,16.0,13.9,12.4,11.2,10.2],
    "10-5":[44.2,27.1,19.3,14.8,11.9,9.9,8.4,7.2,6.4],
    "10-4s":[46.4,30.1,22.7,18.4,15.6,13.6,12.1,11.0,10.0],
    "10-4":[43.4,26.4,18.7,14.3,11.5,9.5,8.1,7.0,6.2],
    "10-3s":[45.5,29.3,22.0,17.8,15.1,13.2,11.8,10.7,9.8],
    "10-3":[42.4,25.5,18.0,13.7,11.0,9.1,7.8,6.8,6.0],
    "10-2s":[44.7,28.5,21.4,17.4,14.8,13.0,11.6,10.5,9.7],
    "10-2":[41.5,24.7,17.3,13.2,10.6,8.8,7.5,6.6,5.8],
    "9-9":[72.1,53.5,41.1,32.6,26.6,22.4,19.4,17.2,15.6],
    "9-8s":[51.1,36.0,28.5,23.6,20.2,17.8,15.9,14.5,13.4],
    "9-8":[48.4,32.9,25.1,20.1,16.6,14.2,12.3,10.9,9.9],
    "9-7s":[49.5,34.2,26.8,22.1,18.9,16.6,14.9,13.6,12.5],
    "9-7":[46.7,30.9,23.1,18.4,15.1,12.8,11.1,9.8,8.8],
    "9-6s":[47.7,32.3,24.9,20.4,17.4,15.3,13.7,12.4,11.4],
    "9-6":[44.9,28.8,21.2,16.6,13.5,11.4,9.8,8.7,7.8],
    "9-5s":[45.9,30.4,23.2,18.8,16.0,13.9,12.4,11.3,10.3],
    "9-5":[42.9,26.7,19.2,14.8,12.0,10.0,8.5,7.4,6.6],
    "9-4s":[43.8,28.4,21.3,17.3,14.6,12.7,11.3,10.3,9.4],
    "9-4":[40.7,24.6,17.3,13.2,10.5,8.7,7.3,6.4,5.6],
    "9-3s":[43.2,27.8,20.8,16.8,14.3,12.5,11.1,10.1,9.2],
    "9-3":[39.9,23.9,16.7,12.7,10.1,8.3,7.1,6.1,5.4],
    "9-2s":[42.3,27.0,20.2,16.4,13.9,12.2,10.9,9.9,9.1],
    "9-2":[38.9,22.9,16.0,12.1,9.6,8.0,6.8,5.9,5.2],
    "8-8":[69.1,49.9,37.5,29.4,24.0,20.3,17.7,15.8,14.4],
    "8-7s":[48.2,33.9,26.6,22.0,18.9,16.7,15.0,13.7,12.7],
    "8-7":[45.5,30.6,23.2,18.5,15.4,13.1,11.5,10.3,9.3],
    "8-6s":[46.5,32.0,25.0,20.6,17.6,15.6,14.1,12.9,11.9],
    "8-6":[43.6,28.6,21.3,16.9,13.9,11.8,10.4,9.2,8.3],
    "8-5s":[44.8,30.2,23.2,19.1,16.3,14.3,12.9,11.8,10.9],
    "8-5":[41.7,26.5,19.4,15.2,12.4,10.5,9.1,8.1,7.3],
    "8-4s":[42.7,28.1,21.4,17.4,14.8,13.0,11.7,10.6,9.8],
    "8-4":[39.6,24.4,17.5,13.4,10.8,9.0,7.8,6.8,6.1],
    "8-3s":[40.8,26.3,19.8,16.0,13.6,11.9,10.7,9.7,8.9],
    "8-3":[37.5,22.4,15.7,11.9,9.5,7.9,6.7,5.8,5.1],
    "8-2s":[40.3,25.8,19.4,15.7,13.3,11.7,10.5,9.6,8.8],
    "8-2":[36.8,21.7,15.1,11.4,9.1,7.5,6.4,5.6,4.9],
    "7-7":[66.2,46.4,34.4,26.8,21.9,18.6,16.4,14.8,13.7],
    "7-6s":[45.7,32.0,25.1,20.8,18.0,15.9,14.4,13.2,12.3],
    "7-6":[42.7,28.5,21.5,17.1,14.2,12.2,10.8,9.6,8.8],
    "7-5s":[43.8,30.1,23.4,19.4,16.7,14.8,13.4,12.3,11.4],
    "7-5":[40.8,26.5,19.7,15.5,12.8,11.0,9.7,8.7,7.9],
    "7-4s":[41.8,28.2,21.7,17.9,15.3,13.5,12.2,11.2,10.4],
    "7-4":[38.6,24.5,17.9,13.9,11.4,9.7,8.5,7.6,6.8],
    "7-3s":[40.0,26.3,20.0,16.4,14.0,12.3,11.1,10.1,9.3],
    "7-3":[36.6,22.4,16.0,12.3,9.9,8.4,7.2,6.4,5.7],
    "7-2s":[38.1,24.5,18.4,15.0,12.8,11.2,10.1,9.2,8.5],
    "7-2":[34.6,20.4,14.2,10.7,8.6,7.2,6.1,5.4,4.8],
    "6-6":[63.3,43.2,31.5,24.5,20.1,17.3,15.4,14.0,13.1],
    "6-5s":[43.2,30.2,23.7,19.7,17.0,15.2,13.8,12.7,11.9],
    "6-5":[40.1,26.7,20.0,15.9,13.3,11.5,10.2,9.2,8.5],
    "6-4s":[41.4,28.5,22.1,18.4,15.9,14.2,12.9,11.9,11.1],
    "6-4":[38.0,24.7,18.2,14.4,12.0,10.3,9.2,8.3,7.6],
    "6-3s":[39.4,26.5,20.4,16.8,14.5,12.9,11.7,10.8,10.0],
    "6-3":[35.9,22.7,16.4,12.8,10.6,9.1,8.0,7.2,6.5],
    "6-2s":[37.5,24.8,18.8,15.4,13.3,11.8,10.7,9.8,9.1],
    "6-2":[34.0,20.7,14.6,11.2,9.1,7.8,6.8,6.0,5.4],
    "5-5":[60.3,40.1,28.8,22.4,18.5,16.0,14.4,13.2,12.3],
    "5-4s":[41.1,28.8,22.6,18.9,16.5,14.8,13.5,12.5,11.7],
    "5-4":[37.9,25.2,18.8,15.0,12.6,11.0,9.8,8.9,8.2],
    "5-3s":[39.3,27.1,21.1,17.5,15.2,13.7,12.5,11.6,10.8],
    "5-3":[35.8,23.3,17.1,13.6,11.4,9.9,8.8,8.0,7.3],
    "5-2s":[37.5,25.3,19.5,16.1,14.0,12.5,11.4,10.6,9.8],
    "5-2":[33.9,21.3,15.3,12.0,10.0,8.6,7.6,6.8,6.2],
    "4-4":[57.0,36.8,26.3,20.6,17.3,15.2,13.9,12.9,12.1],
    "4-3s":[38.0,26.2,20.3,16.9,14.7,13.1,12.0,11.1,10.3],
    "4-3":[34.4,22.3,16.3,12.8,10.7,9.3,8.3,7.5,6.8],
    "4-2s":[36.3,24.6,18.8,15.7,13.7,12.3,11.2,10.4,9.6],
    "4-2":[32.5,20.5,14.7,11.5,9.5,8.3,7.3,6.6,6.0],
    "3-3":[53.7,33.5,23.9,19.0,16.2,14.6,13.5,12.6,12.0],
    "3-2s":[35.1,23.6,18.0,14.9,13.0,11.7,10.7,9.9,9.2],
    "3-2":[31.2,19.5,13.9,10.8,8.9,7.7,6.8,6.1,5.6],
    "2-2":[50.3,30.7,22.0,17.8,15.5,14.2,13.3,12.5,12.0]
    }

class Hand : 
    def __init__(self, hand):
        self._cards = hand
        self.sortByRank()

    def __add__(self, other) :
        return self._cards + other._cards

    def __setitem__(self, item, value):
        self._cards[item]=value

    def __getitem__(self, item):
        return self._cards[item]
    
    def __str__(self) :
        if self._cards[0].suit == self._cards[1].suit :
            return str(self._cards[0])+"-"+str(self._cards[1])+'s'
        return str(self._cards[0])+"-"+str(self._cards[1])

    def sortByRank(self) : 
        if self._cards[1].suit > self._cards[0].suit :
            self._cards = [self._cards[1], self._cards[0]]
        elif self._cards[1].rank == self._cards[0].rank and self._cards[1].suit > self._cards[0].suit :
            self._cards = [self._cards[1], self._cards[0]]
    
class Table :
    def __init__(self, cards = None) :
        if cards is None :
            self._cards = [None] * 5
        else :
            self._cards = cards

    def __add__(self, other) :
        return self._cards + other._cards

    def __setitem__(self, item, value):
        self._cards[item]=value

    def __len__(self) :
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]
    
    def getQuinteFlushValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        for subs in combinations(cards, 5) :
            suits = set(card.suit for card in subs)
            if len(suits) == 1:
                ranks = sorted(card.rank for card in subs)
                if all(ranks[i] == ranks[i-1] + 1 for i in range(1, len(ranks))) :
                    rank = max(rank, ranks[-1])
        return [rank]
    
    def getFourOfAKindValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(5) :
            sub_ranks = ranks_sorted[i:i+4]
            if all(sub_ranks[i] == sub_ranks[i-1] for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return [rank]
    
    def getFullHouseValue(self, hand : Hand):
        cards = self + hand
        rank_3, rank_2 = -1, -1
        for subs in combinations(cards, 5):
            ranks = sorted(card.rank for card in subs)
            if len(set(ranks)) == 2:
                count_1 = ranks.count(ranks[0])
                count_2 = ranks.count(ranks[-1])
                if (count_1 == 2 and count_2 == 3) or (count_1 == 3 and count_2 == 2):
                    rank_3 = max(rank_3, ranks[2])
                    rank_2 = max(rank_2, ranks[0 if count_1 == 2 else -1])
        return [rank_3, rank_2]
    
    def getFlushValue(self, hand : Hand) :
        cards = self + hand
        rank = [-1]*5
        for subs in combinations(cards, 5) :
            suits = set(card.suit for card in subs)
            if len(suits) == 1 :
                ranks = sorted([card.rank for card in cards], reverse=True)
                j = 0
                while ranks[j] == rank[j] and j < 5:
                    j+=1
                if j < 5 and ranks[j] > rank[j] :
                    rank = ranks
        return rank

    def getStraightValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(4) :
            sub_ranks = ranks_sorted[i:i+5]
            if all(sub_ranks[i] == sub_ranks[i-1] + 1 for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return [rank]
    
    def getThreeOfAKindValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(6) :
            sub_ranks = ranks_sorted[i:i+3]
            if all(sub_ranks[i] == sub_ranks[i-1] for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return [rank]

    def getDoublePairValue(self, hand : Hand) :
        cards = self + hand
        rank1, rank2 = -1, -1
        for subs in combinations(cards, 4) :
            ranks = sorted(card.rank for card in subs)
            count_1 = ranks.count(ranks[0])
            count_2 = ranks.count(ranks[-1])
            if count_1 == 2 and count_2 == 2 :
                rank2 = max(ranks[-1], rank2)
                rank1 = max(ranks[0], rank1)
        return [rank2, rank1]
            
    def getPairValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        for subs in combinations(cards, 2):
            ranks = set(card.rank for card in subs)
            if len(ranks) == 1 :
                rank = max(rank, list(ranks)[-1])
        return [rank]
    
    def getHighCardValue(self, hand : Hand) :
        cards = self + hand
        return [sorted(card.rank for card in cards)[-1]]
    
    funcs = [getQuinteFlushValue, getFourOfAKindValue,
                     getFullHouseValue, getFlushValue, getStraightValue,
                     getThreeOfAKindValue, getDoublePairValue,
                     getPairValue, getHighCardValue]
    shifts = [56, 52, 44, 24, 20, 16, 8, 4, 0]

    """
        
    Value de rank pour la plupart a besoin de 13 valeurs différent : 4 bits
    Value de rank pour getFullHouseValue a besoin de 8 bits (13 * 12)
    Valeur de getFlushValue a besoin de 13*12*11*10*9 -> 20 bits
    Valeur de getDoublePairValue a besoin de 8 bits

    Dans l'ordre :
    - 4 bits QuinteFlush
    - 4 bits FourOfAKind
    - 8 bits FullHouse
    - 20 bits Flush
    - 4 bits Straight
    - 4 bits ThreeOfAKind
    - 8 bits DoublePair
    - 4 bits Pair
    - 4 bits HighCard

    -> 60 bits

    """
    def getHighestValue(self, hand : Hand) :
        i = 0
        while i < len(Table.funcs) :
            value = Table.funcs[i](self, hand)
            if value[0] > -1 :
                ret = 0
                for j in range(len(value)) :
                    ret += value[j] << (len(value)-1-j)*4
                return ret << Table.shifts[i]
            i += 1

class Card :

    ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 
    suits=['h', 'c', 's', 'd']

    def __init__(self, rank, suit) :
        if isinstance(rank, int) :
            self.rank = rank
        else :
            self.rank = Card.ranks.index(rank)
        if isinstance(suit, int) :
            self.suit = suit
        else :
            self.suit = Card.suits.index(suit)

    def __str__ (self) :
        return self.ranks[self.rank]+self.suits[self.suit]

    def getRank(self) : 
        return self.rank
    
if __name__ == "__main__" :
    from utils import saveDictToFile, loadDictFromFile

    data_path = "D:/Poker Project/Project/Data/pre-flop.json"

    deck = [Card(i%13,i//13) for i in range(13*4)]
    storage = loadDictFromFile(data_path)
    for sub in combinations(deck, 2) :
        storage[str(Hand(sub))] = 0

    def getSampleAndRemove(k, list) :
        ans = []
        for _ in range(k) :
            card_index = rd.randint(0, len(list)-1)
            ans.append(list[card_index])
            del list[card_index]
        return ans

    nb_players = 2
    
    nb_try = 100000

    #orig_hand = Hand([Card(0, 0), Card(1,1)])
    #print(str(orig_hand[0]), str(orig_hand[1]))

    
    current_time = time.time()
    for n in range(nb_try) :
        #hands = [orig_hand]
        hands = []
        print(f"{int(n/nb_try*100*100)/100}%", end="\r")
        #available = [Card(i%13,i//13) for i in range(13*4) if all(i%13 != hands[0][j].rank or i%4 != hands[0][j].suit for j in [0,1])]
        available = [Card(i%13,i//13) for i in range(13*4)]

        for i in range(nb_players) :
            hands.append(Hand(getSampleAndRemove(2, available)))

        table = Table(getSampleAndRemove(5, available))
        values = [table.getHighestValue(hand) for hand in hands]

        max_indexes, max_value = [0], values[0]
        for i in range(len(values)) :
            if values[i] > max_value :
                max_indexes, max_value = [i], values[i]
                break
            elif values[i] == max_value :
                max_indexes += [i]

        for ind in max_indexes :
            storage[str(hands[ind])] += 1/len(max_indexes)

    print(f"Elapsed Time : {int((time.time() - current_time)*100)/100}s")
    #print(f"{int(nb_won/nb_try*100*100)/100}%")
    storage["nb_try"] += nb_try
    print(storage)
    saveDictToFile(storage, data_path)