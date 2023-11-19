class Table :
    def __init__(self) :
        self._cards = [None] * 5   

    def __setitem__(self, item, value):
        self._cards[item]=value

    def __len__(self) :
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]

    def getPairValue(self, hand : Hand) :
        for i in [0,1] :
            for j in range(len(self._cards)) :
                if hand[i].rank == self[j].rank :
                    return (hand[i].rank)
        return -1

    def getDoublePairValue(self, hand : Hand) :
        index1 = 
        index2 = 

class Hand : 
    def __init__(self, hand):
        self._lst = hand

    def __setitem__(self, item, value):
        self._lst[item]=value

    def __getitem__(self, item):
        return self._lst[item]
        
class Card :

    ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits=['h', 'c', 's', 'd']

    def __init__(self, rank, suit) : 
        self.rank = Card.ranks.index(rank)
        self.suit = Card.suits.index(suit)

    def __str__ (self) :
        return str(self.rank)+str(self.suit)

    def getRank(self) : 
        return self.rank

    

