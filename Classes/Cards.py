from itertools import combinations

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

class Table :
    def __init__(self) :
        self._cards = [None] * 5   

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
        return rank
    
    def getFourOfAKindValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(5) :
            sub_ranks = ranks_sorted[i:i+4]
            if all(sub_ranks[i] == sub_ranks[i-1] for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return rank
    
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
        return rank_3, rank_2
    
    def getFlushValue(self, hand : Hand) :
        cards = self + hand
        rank = [-1]*5
        for subs in combinations(cards, 5) :
            suits = set(card.suit for card in subs)
            if len(suits) == 1 :
                ranks = sorted([card.rank for card in cards], reverse=True)
                j = 0
                while ranks[j] == rank[j] :
                    j+=1
                if j < 5 and ranks[j] > rank[j] :
                    rank = ranks

    def getStraightValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(4) :
            sub_ranks = ranks_sorted[i:i+5]
            if all(sub_ranks[i] == sub_ranks[i-1] + 1 for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return rank
    
    def getThreeOfAKindValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        ranks_sorted = sorted(card.rank for card in cards)
        for i in range(6) :
            sub_ranks = ranks_sorted[i:i+3]
            if all(sub_ranks[i] == sub_ranks[i-1] for i in range(1, len(sub_ranks))) :
                rank = max(rank, sub_ranks[-1])
        return rank

    def getDoublePairValue(self, hand : Hand) :
        cards = self + hand
        rank1, rank2 = -1, -1
        for subs in combinations(cards, 4) :
            ranks = sorted(card.rank for card in subs)
            count_1 = ranks.count(ranks[0])
            count_2 = ranks.count(ranks[-1])
            if count_1 == 2 and count_1 == 2 :
                rank2 = max(ranks[-1], rank2)
                rank1 = max(ranks[0], rank1)
        return rank2, rank1
            
    def getPairValue(self, hand : Hand) :
        cards = self + hand
        rank = -1
        for subs in combinations(cards, 2):
            ranks = set(card.rank for card in subs)
            if len(ranks) == 1 :
                rank = max(rank, ranks[-1])
        return rank
    
    def getHighCardValue(self, hand : Hand) :
        cards = self + hand
        return sorted(card.rank for card in cards)[-1]

class Card :

    ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    #ranks=[i for i in range(13)] #Plus simple pour comparer les cartes 
    suits=['h', 'c', 's', 'd']

    def __init__(self, rank, suit) :
        self.rank = Card.ranks.index(rank)
        self.suit = Card.suits.index(suit)

    def __str__ (self) :
        return str(self.rank)+str(self.suit)

    def getRank(self) : 
        return self.rank
    
if __name__ == "__main__" :
    

    

