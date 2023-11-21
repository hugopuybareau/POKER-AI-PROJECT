import json

def loadDictFromFile(filename):
    try:
        with open(filename, 'r') as file:
            loaded_dict = json.load(file)
        if loaded_dict is None :
            return {}
        else :
            return loaded_dict
    except :
        print(f"No file found, empty dictionnary provided")
        return {}

def saveDictToFile(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

"""
C'est Bayes en gros :
P(Gagner | Main=(card1,card2)) = P(Gagner)*P(Main=(card1,card2) | Gagner) / P(Main=(card1,card2))
= 1/nb_player * sum(storage[cartes qui t'intéressent])/nb_try * (2 parmi 52) / (2 parmi nb_cartes_qui_intéressent)
"""
def computeProba(keys, dictionnary) :
    sum = 0
    for key in keys :
        sum += dictionnary[key]
    
    return 2*sum/dictionnary["nb_try"]/dictionnary["nb_player"]*1326/len(keys)/(len(keys)-1)