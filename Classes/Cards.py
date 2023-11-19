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
        if hand[0].rank == hand[1].rank :
            return hand[0].rank
        for i in [0, 1] :
            for j in range(len(self._cards)) :
                if hand[i].rank == self[j].rank :
                    return (hand[i].rank)
        return -1

    def getDoublePairValue(self, hand : Hand) :
        rank1 = -1
        rank2 = -1
        if hand[0].rank == hand[1].rank :
            rank1 = hand[0].rank
        for i in [0, 1]:
            for j in range(len(self._cards)):
                if hand[i].rank == self[j].rank : 
                    rank2 = hand[i].rank
                if rank1 == -1 : 
                    rank1, rank2 = rank2, rank1
        if rank1 < rank2 : 
            rank1, rank2 = rank2, rank1 
        return [rank1, rank2]

    
    def getThreeOfAKindValue(self, hand : Hand) :
        if hand[0].rank == hand[1].rank : #pair in the hand
            for j in range(len(self._cards)) : 
                if hand[0].rank == self[j].rank : 
                    return hand[0].rank
        for i in [0, 1] : #pair on the table
            for j in range(len(self._cards)) : 
                for k in range(len(self._cards)) : 
                    if hand[i].rank==self[j].rank==self[k].rank :
                        return hand[0].rank
        for i in range(len(self._cards)) : #Three of a kind on the table
            for j in range(len(self._cards)) : 
                for k in range(len(self._cards)) : 
                    if self[i].rank==self[j].rank==self[k].rank :
                        return self[i].rank 
        return -1 #Not threeOfAKind
    
    def getStraightValue(self, hand : Hand) : #I want the function to be able to recognize wether and straight index is associated to a hand card or a table card
        for i in range(9):
            straight = [k for k in range (i, i+5)] 

        



class Hand : 
    def __init__(self, hand):
        self._lst = hand

    def __setitem__(self, item, value):
        self._lst[item]=value

    def __getitem__(self, item):
        return self._lst[item]
    
    def sortByRank(self) : 
        if self._lst[1].rank > self._lst[0].rank :
            self._lst[0], self._lst[1] = self._lst[1], self._lst[0]

        
class Card :

    ranks=[i for i in range(13)] #Plus simple pour comparer les cartes 
    suits=['h', 'c', 's', 'd']

    def __init__(self, rank, suit) : 
        self.rank = Card.ranks.index(rank)
        self.suit = Card.suits.index(suit)

    def __str__ (self) :
        return str(self.rank)+str(self.suit)

    def getRank(self) : 
        return self.rank

    

