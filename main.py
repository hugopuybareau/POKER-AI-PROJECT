from Classes.Game import *
from Classes.utils import *

a=3

if __name__ == "__main__" :
    print("Ouaaaaaaaiiiiis c'est michel, tu donnes pas de nouvelles")
    print("Nie nie nie moi c'est le client j'ai besoin qu'on m'epelle les mots sinon je comprends pas")

    storage = loadDictFromFile(data_path)

    print(computeProba([""], storage))