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