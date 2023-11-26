#from Classes.Game import *
from Classes.utils import *
from Classes.Cards import *

a=3

if __name__ == "__main__" :
    print("Ouaaaaaaaiiiiis c'est michel, tu donnes pas de nouvelles")
    print("Nie nie nie moi c'est le client j'ai besoin qu'on m'epelle les mots sinon je comprends pas")

    """nb_players = 3
    data_path = f"D:/Poker Project/Project/Data/pre-flop_{nb_players}.json"

    storage = loadDictFromFile(data_path)

    keys = Hand.generateAllKeysFromRanks("2-7", suited=None)
    print(storage)
    print(keys)
    print(computeProba(keys, storage))

    current_time = time.time()
    for i in range(100000000) :
        Card(i%13,i%4)
    print(time.time()-current_time)"""
    current_time = time.time()
    for i in range(10000000) :
        
    print(time.time()-current_time)