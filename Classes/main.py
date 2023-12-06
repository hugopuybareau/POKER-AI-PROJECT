#from Classes.Game import *
from utils import getSampleAndRemove
from Cards import Card, Hand, Table
from Proba import Proba
import time
from itertools import combinations
import random
import numpy as np
import matplotlib.pyplot as plt

#Il est IMPORTANT de mettre en première les deux cartes de la main du joueur
def playCards(nb_players, nb_try, turnvalues, cards_str=None) :

    current_time = time.time()
    orig_hands = [None]*nb_players
    if cards_str is not None :
        arr = cards_str.strip().split("-")
        cards = [Card.initFromStr(c_str) for c_str in arr]
        orig_hands[-1] = Hand(cards[:2])
        cards = cards[2:]
        nb_players -= 1
    else :
        arr = []
        cards=[]

    count = 0
    rng = range(0, 52)
    for n in range(nb_try) :
        random_array = random.sample(rng, k=5+2*nb_players-len(cards))
        hands = orig_hands
        if n % 1000 == 0 :
            print(f"{int(n/nb_try*100*100)/100}%, {time.time()-current_time}", end="\r")
        available = [Card(i%13,i//13) for i in random_array]
        sample, available = getSampleAndRemove(nb_players*2, available)
        for i in range(nb_players) :
            hands[i] = Hand(sample[i*2:i*2+2])

        table = Table(available+cards)
        values = [table.v3_getHighestValue(hand, turnvalues) for hand in hands]

        max_indexes, max_value = [0], values[0]
        for i in range(1, len(values)) :
            if values[i] > max_value :
                max_indexes, max_value = [i], values[i]
            elif values[i] == max_value :
                max_indexes += [i]
            
        if len(values)-1 in max_indexes :
            count+=1
    print(f"Elapsed Time : {int((time.time() - current_time)*100)/100}s")
    return count/nb_try#Il est IMPORTANT de mettre en première les deux cartes de la main du joueur

def playCardsAndFill(nb_players, nb_try, turnvalues, cards, folder_path = f"D:/Poker Project/poker_project/Data/hands") :
    flop_data_length = 2598960
    folder_path = f"{folder_path}/{nb_players}"
    hand = Hand(cards)
    path = folder_path+"/"+str(hand)
    proba = Proba.loadOrSetupBlank(path, data_length=flop_data_length)
    fillCards(nb_players, nb_try, turnvalues, hand, proba)
    proba.writeSegments()

def fillCards(nb_players, nb_try, turnvalues, cards, proba : Proba) :
    cards_code = [(card.rank, card.suit) for card in cards]
    rng = [i for i in range(52) if (i%13,i//13) not in cards_code]
    current_time = time.time()
    orig_hands = [None]*nb_players
    orig_hands[-1] = Hand(cards[:2])
    cards = cards[2:]
    nb_players -= 1

    for n in range(nb_try) :
        random_array = random.sample(rng, k=5+2*nb_players-len(cards))
        hands = orig_hands
        if n % 1000 == 0 :
            print(f"{int(n/nb_try*100*100)/100}%, {time.time()-current_time}", end="\r")
        available = [Card(i%13,i//13) for i in random_array]
        sample, available = getSampleAndRemove(nb_players*2, available)
        for i in range(nb_players) :
            hands[i] = Hand(sample[i*2:i*2+2])

        table = Table(available+cards)
        try :
            values = [table.v3_getHighestValue(hand, turnvalues) for hand in hands]
        except :
            print(Table.explicitValue(table), str(orig_hands[-1]))

        max_indexes, max_value = [0], values[0]
        for i in range(1, len(values)) :
            if values[i] > max_value :
                max_indexes, max_value = [i], values[i]
            elif values[i] == max_value :
                max_indexes += [i]
        
        if len(values)-1 in max_indexes :
            proba.addValuesOneD(Proba.getId5Cards(table._cards), 1, 1)
        else :
            proba.addValuesOneD(Proba.getId5Cards(table._cards), 0, 1)

def fillEveryHand(nb_players, nb_try, turnvalues, folder_path = f"D:/Poker Project/poker_project/Data/hands") :
    deck = [Card(i%13,i//13) for i in range(52)]
    flop_data_length = 2598960
    folder_path = f"{folder_path}/{nb_players}"
    i = 1
    for sub in combinations(deck, 2) :
        current_time = time.time()
        hand = Hand(list(sub))
        path = folder_path+"/"+str(hand)
        proba = Proba.loadOrSetupBlank(path, data_length=flop_data_length)
        fillCards(nb_players, nb_try, turnvalues, hand._cards, proba)
        proba.writeSegments()
        print(f"{i}/{1326}, Elapsed Time : {int((time.time() - current_time)*100)/100}s", end="\r")
        i+=1

turnvalues = Proba.loadOrSetupBlank(f"D:/Poker Project/poker_project/Data/turnvalues", 133784560)#2598960)
fillEveryHand(2, 10000, turnvalues)
raise

def readOrComputeProba(cards_str, nb_players) :
    cards = Table.initFromKey(cards_str)
    if len(cards) == 2 :
        preflop_data_length = 1326
        p_preflop = f"D:/Poker Project/poker_project/Data/pre-flop/{nb_players}"
        proba_preflop = Proba.loadOrSetupBlank(p_preflop, data_length=preflop_data_length)

if __name__ == "__main__" :
    print("Ouaaaaaaaiiiiis c'est michel, tu donnes pas de nouvelles")
    print("Nie nie nie moi c'est le client j'ai besoin qu'on m'epelle les mots sinon je comprends pas")

    nb_players = 2
    nb_try = 100000

    deck = [Card(i%13,i//13) for i in range(52)]

    turnvalues = Proba.loadOrSetupBlank(f"D:/Poker Project/poker_project/Data/turnvalues", 133784560)#2598960)
    """i = 0
    for sub in combinations(deck, 7) :
        if i % 20000 == 0 :
            print(i/133784560*100, end="\r")
        table = Table(sub)
        id = Proba.getIdCards(table._cards)
        turnvalues.setValuesOneD(id, table.new_getHighestValue(), 0)
        i+=1
    turnvalues.writeSegments()
    raise"""

    current_time = time.time()
    preflop_data_length = 1326
    p_preflop = f"D:/Poker Project/poker_project/Data/pre-flop/{nb_players}"
    proba_preflop = Proba.loadOrSetupBlank(p_preflop, data_length=preflop_data_length)
    print(f"Loaded pre-flop in {time.time()-current_time}s")

    current_time = time.time()
    flop_data_length = 2598960
    p_flop = f"D:/Poker Project/poker_project/Data/flop/{nb_players}"
    proba_flop = Proba.loadOrSetupBlank(p_flop, data_length=flop_data_length)
    print(f"Loaded flop in {time.time()-current_time}s")

    print(proba_flop.readValuesOneD(proba_flop.getIdFromKey("2c-4h-7h-8h-9h")))

    current_time = time.time()
    river_data_length = 20358520
    p_river = f"D:/Poker Project/poker_project/Data/river/{nb_players}"
    proba_river = Proba.loadOrSetupBlank(p_river, data_length=river_data_length)
    print(f"Loaded river in {time.time()-current_time}s")

    current_time = time.time()
    turn_data_length = 133784560
    p_turn = f"D:/Poker Project/poker_project/Data/turn/{nb_players}"
    proba_turn = Proba.loadOrSetupBlank(p_turn, data_length=turn_data_length)
    print(f"Loaded turn in {time.time()-current_time}s")

    arr = range(0, 52)
    def run() :
        current_time = time.time()
        for n in range(nb_try) :
            random_array = random.sample(arr, k=5+2*nb_players)
            hands = [None]*nb_players
            if n % 10000 == 0 :
                print(f"{int(n/nb_try*100*100)/100}%, {time.time()-current_time}", end="\r")
            available = [Card(i%13,i//13) for i in random_array]

            sample, available = getSampleAndRemove(nb_players*2, available)
            for i in range(nb_players) :
                hands[i] = Hand(sample[i*2:i*2+2])

            table = Table(available)
            values = [table.v3_getHighestValue(hand, turnvalues) for hand in hands]

            max_indexes, max_value = [0], values[0]
            for i in range(1, len(values)) :
                if values[i] > max_value :
                    max_indexes, max_value = [i], values[i]
                elif values[i] == max_value :
                    max_indexes += [i]
                
            ids_preflop = [Proba.getIdCards(hand._cards) for hand in hands]
            ids_flop = [Proba.getIdCards(hand._cards+table._cards[:3]) for hand in hands]
            ids_river = [Proba.getIdCards(hand._cards+table._cards[:4]) for hand in hands]
            ids_turn = [Proba.getIdCards(hand._cards+table._cards) for hand in hands]

            for ind in max_indexes :
                proba_preflop.addValuesOneD(ids_preflop[ind], 1, 0)
                proba_flop.addValuesOneD(ids_flop[ind], 1, 0)
                proba_river.addValuesOneD(ids_river[ind], 1, 0)
                proba_turn.addValuesOneD(ids_turn[ind], 1, 0)
            for i in range(nb_players) :
                proba_preflop.addValuesOneD(ids_preflop[i], 0, 1)
                proba_flop.addValuesOneD(ids_flop[i], 0, 1)
                proba_river.addValuesOneD(ids_river[i], 0, 1)
                proba_turn.addValuesOneD(ids_turn[i], 0, 1)

        print(f"Elapsed Time : {int((time.time() - current_time)*100)/100}s")

        print(proba_flop.readValuesOneD(proba_flop.getIdFromKey("2c-4h-7h-8h-9h")))

        print("Pre-flop", proba_preflop.stats())
        print("Flop", proba_flop.stats())
        print("River", proba_river.stats())
        print("Turn", proba_turn.stats())

        current_time = time.time()
        proba_preflop.writeSegments()
        proba_flop.writeSegments()
        proba_river.writeSegments()
        proba_turn.writeSegments()
        print(f"Saved in {time.time()-current_time}s")

    import cProfile
    #cProfile.run('run()', sort='cumulative')
    run()
    
    """user_input = ""
    while True :
        nb_players = input("Enter nb_players : ")
        if nb_players in ["e", "ex", "exi", "exit", "quit", "stop"] :
            break
        user_input = input("Enter cards : ")
        if user_input in ["e", "ex", "exi", "exit", "quit", "stop"] :
            break
        try :
            cards = Table.initFromStr(user_input)
            if len(cards) == 2 :
                print(computeProbaPreFlop(int(nb_players), cards))
            elif len(cards) == 5 :
                print(computeProbaFlop(int(nb_players), cards))
            elif len(cards) == 6 :
                print(computeProbaRiver(int(nb_players), cards))
        except :
            print("Error ! If you want to exit, type exit")
    
    print(time.time()-current_time)"""
    