#from Classes.Game import *
from utils import loadDictFromFile, getSampleAndRemove, saveDictToFile
from Cards import Card, Hand, Table
from Proba import Proba
import time
from itertools import combinations
import random
import numpy as np
import matplotlib.pyplot as plt

a=3

if __name__ == "__main__" :
    print("Ouaaaaaaaiiiiis c'est michel, tu donnes pas de nouvelles")
    print("Nie nie nie moi c'est le client j'ai besoin qu'on m'epelle les mots sinon je comprends pas")

    nb_players = 2
    nb_try = 1000000

    deck = [Card(i%13,i//13) for i in range(52)]

    """turnvalues = Proba.loadOrSetupBlank(f"D:/Poker Project/poker_project/Data/turnvalues", 133784560)#2598960)
    i = 0
    for sub in combinations(deck, 7) :
        if i % 20000 == 0 :
            print(i/133784560*100, end="\r")
        table = Table(sub)
        id = Proba.getIdCards(table._cards)
        turnvalues.setValuesOneD(id, table.new_getHighestValue(), 0)
        i+=1
    turnvalues.writeSegments()
    raise"""

    """preflop_data_path = f"D:/Poker Project/poker_project/Data/pre-flop_{nb_players}.json"
    storage_preflop = loadDictFromFile(preflop_data_path)
    for sub in combinations(deck, 2) :
        name = str(Table(sub))
        if not name in storage_preflop :
            storage_preflop[name] = [0,0]
        else :
            break"""

    current_time = time.time()
    preflop_data_length = 1326
    p_preflop = f"D:/Poker Project/poker_project/Data/pre-flop/{nb_players}"
    proba_preflop = Proba.loadOrSetupBlank(p_preflop, data_length=preflop_data_length)
    print(f"Loaded pre-flop in {time.time()-current_time}s")

    print(proba_preflop.getIdFromKey("2c-4h"))
    print(proba_preflop.readValuesOneD(proba_preflop.getIdFromKey("2c-4h")))


    """for i in range(preflop_data_length):
        print(proba_preflop.readValuesOneD(i))
    raise"""

    """current_time = time.time()
    flop_data_length = 2598960
    p_flop = f"D:/Poker Project/poker_project/Data/flop/{nb_players}"
    proba_flop = Proba.loadOrSetupBlank(p_flop, data_length=flop_data_length)
    print(f"Loaded flop in {time.time()-current_time}s")

    current_time = time.time()
    river_data_length = 20358520
    p_river = f"D:/Poker Project/poker_project/Data/river/{nb_players}"
    proba_river = Proba.loadOrSetupBlank(p_river, data_length=river_data_length)
    print(f"Loaded river in {time.time()-current_time}s")

    current_time = time.time()
    turn_data_length = 133784560
    p_turn = f"D:/Poker Project/poker_project/Data/turn/{nb_players}"
    proba_turn = Proba.loadOrSetupBlank(p_turn, data_length=turn_data_length)
    print(f"Loaded turn in {time.time()-current_time}s")"""

    """print(proba_preflop.readProba("2c-4h"))
    print(storage_preflop["2c-4h"][0]/storage_preflop["2c-4h"][1])"""
    
    """current_time = time.time()
    flop_data_path = f"D:/Poker Project/poker_project/Data/flop_{nb_players}.json"
    storage_flop = loadDictFromFile(flop_data_path)
    for sub in combinations(deck, 5) :
        name = str(Table(sub))
        if not name in storage_flop :
            storage_flop[name] = [0,0]
        else :
            break
    print(f"Loaded flop in {time.time()-current_time}s")
    
    current_time = time.time()
    river_data_path = f"D:/Poker Project/poker_project/Data/river_{nb_players}.json"
    storage_river = loadDictFromFile(river_data_path)
    for sub in combinations(deck, 6) :
        name = str(Table(sub))
        if not name in storage_river :
            storage_river[name] = [0,0]
        else :
            break
    print(f"Loaded river in {time.time()-current_time}s")"""

    arr = range(0, 52)
    val = [0,0]
    def run() :
        """def sort_one(available):
            sample, available = getSampleAndRemove(6, available)
            hands = [None]*nb_players
            for i in range(nb_players) :
                hands[i] = Hand(sample[i*2:i*2+2])
            return hands
        def sort_two(available):
            hands = [None]*nb_players
            for i in range(nb_players) :
                sample, available = getSampleAndRemove(2, available)
                hands[i] = Hand(sample)
            return hands
        random_array = random.sample(arr, k=5+2*nb_players)
        available = [Card(i%13,i//13) for i in random_array]
        sample, available = getSampleAndRemove(7, available)
        for i in range(1000000) :
            if i%1000 == 0 :
                print(i/1000000*100, end="\r")
            random_array = random.sample(arr, k=5+2*nb_players)
            available = [Card(i%13,i//13) for i in random_array]
            #id_one = sort_one(available)
            id_two = sort_two(available)
        raise"""
        current_time = time.time()
        for n in range(nb_try) :
            random_array = random.sample(arr, k=5+2*nb_players)
            #hands = [orig_hand]
            hands = [None]*nb_players
            if n % 10000 == 0 :
                print(f"{int(n/nb_try*100*100)/100}%, {time.time()-current_time}", end="\r")
            #available = [Card(i%13,i//13) for i in range(13*4) if all(i%13 != hands[0][j].rank or i%4 != hands[0][j].suit for j in [0,1])]
            available = [Card(i%13,i//13) for i in random_array]

            sample, available = getSampleAndRemove(nb_players*2, available)
            for i in range(nb_players) :
                hands[i] = Hand(sample[i*2:i*2+2])

            table = Table(available)
            #table.setupStr()
            #values = [table.getHighestValue(hand) for hand in hands]
            #explicit = [Table.explicitValue(value) for value in values]
            #values = [table.v3_getHighestValue(hand, turnvalues) for hand in hands]
            values = [table.new_getHighestValue(hand) for hand in hands]
            
            #explicit = [Table.explicitValue(value) for value in values]

            max_indexes, max_value = [0], values[0]
            for i in range(1, len(values)) :
                if values[i] > max_value :
                    max_indexes, max_value = [i], values[i]
                elif values[i] == max_value :
                    max_indexes += [i]
                
            ids_preflop = [Proba.getIdCards(hand._cards) for hand in hands]
            """ids_flop = [Proba.getIdCards(hand._cards+table._cards[:3]) for hand in hands]
            #print(ids_flop)
            ids_river = [Proba.getIdCards(hand._cards+table._cards[:4]) for hand in hands]
            #print(ids_river)
            ids_turn = [Proba.getIdCards(hand._cards+table._cards) for hand in hands]
            #print(ids_turn)"""

            for ind in max_indexes :
                """storage_river[str(Table(hands[ind]._cards+table._cards[:4]))][0] += int(1000/len(max_indexes))/1000
                storage_flop[str(Table(hands[ind]._cards+table._cards[:3]))][0] += int(1000/len(max_indexes))/1000"""
                #storage_preflop[str(hands[ind])][0] += 1
                """if ids_preflop[ind] == 57 :
                    print(f"Table : {table}, hands : {','.join(str(hand) for hand in hands)}")
                    print(explicit)
                    val[0] += 1"""
                proba_preflop.addValuesOneD(ids_preflop[ind], 1, 0)
                """proba_flop.addValuesOneD(ids_flop[ind], 1, 0)
                proba_river.addValuesOneD(ids_river[ind], 1, 0)
                proba_turn.addValuesOneD(ids_turn[ind], 1, 0)"""
            for id in ids_preflop :
                """if id == 57 :
                    val[1] += 1"""
                proba_preflop.addValuesOneD(id, 0, 1)
            """for id in ids_flop :
                proba_flop.addValuesOneD(id, 0, 1)
            for id in ids_river :
                proba_river.addValuesOneD(id, 0, 1)
            for id in ids_turn :
                proba_turn.addValuesOneD(id, 0, 1)"""
                #storage_river[str(Table(hand._cards+table._cards[:4]))][1] += 1
                #storage_flop[str(Table(hand._cards+table._cards[:3]))][1] += 1

        print(f"Elapsed Time : {int((time.time() - current_time)*100)/100}s")
        print(val)
        """if not "nb_try" in storage_preflop :
            storage_preflop['nb_try'] = 0
        storage_preflop["nb_try"] += nb_try
        storage_preflop["nb_players"] = nb_players"""

        """if not "nb_try" in storage_flop :
            storage_flop['nb_try'] = 0
        storage_flop["nb_try"] += nb_try
        storage_flop["nb_players"] = nb_players

        if not "nb_try" in storage_river :
            storage_river['nb_try'] = 0
        storage_river["nb_try"] += nb_try
        storage_river["nb_players"] = nb_players"""
        #print(storage)
        """print(proba_preflop.readValuesWhole("2c-4h"))
        print(storage_preflop["2c-4h"])
        current_time = time.time()
        saveDictToFile(storage_preflop, preflop_data_path)
        print(f"Saved pre-flop in {time.time()-current_time}s")"""

        proba_preflop.writeSegments()

        print(proba_preflop.getIdFromKey("2c-4h"))
        print(proba_preflop.readValuesOneD(proba_preflop.getIdFromKey("2c-4h")))
        """proba_flop.writeSegments()
        proba_river.writeSegments()
        proba_turn.writeSegments()"""

        """plt.subplot(1, 4, 1)
        plt.imshow(proba_preflop.image)
        plt.subplot(1, 4, 2)
        plt.imshow(proba_flop.image)
        plt.subplot(1, 4, 3)
        plt.imshow(proba_river.image)
        plt.subplot(1, 4, 4)
        plt.imshow(proba_river.image)
        plt.show()"""
        """current_time = time.time()
        saveDictToFile(storage_flop, flop_data_path)
        print(f"Saved flop in {time.time()-current_time}s")
        current_time = time.time()
        saveDictToFile(storage_river, river_data_path)
        print(f"Saved river in {time.time()-current_time}s")"""
        

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
    