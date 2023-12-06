import time
import cv2
from itertools import combinations
import numpy as np
from Cards import Card, Table
from utils import loadDictFromFile
import os
import pyexr

class Proba :
    #Defined Function
    SEGMENT_SIZE = 512

    def __init__(self, path, loadSegments=False, loadWhole=True) :
        self.images = None
        self.image = None
        self.one_d = None
        """if data_length is not None :
            self = Proba.setupBlank(path, data_length, loadSegments=loadSegments)
            return
        elif os.path.exists(f"{path}_{int(np.sqrt(data_length))+1}") :
            path = f"{path}_{int(np.sqrt(data_length))+1}"""
        self._path = path
        self.side = int(path.split("_")[-1])
        temp = self.side/Proba.SEGMENT_SIZE
        if temp % 1 == 0 :
            self.size = int(temp)
        else :
            self.size = int(temp)+1

        if loadSegments :
            self.loadSegments()
        elif loadWhole :
            self.loadWhole()

    def thresh(self, threshold) :
        if self.one_d is not None :
            return 100-np.count_nonzero(self.one_d[:,1] < threshold)/self.one_d.shape[0]*100
        elif self.image is not None :
            return 100-np.count_nonzero(self.image[:,:,1] < threshold)/self.image.shape[0]/self.image.shape[1]*100
        else :
            return -1

    def loadWhole(self, image=None) :
        if image is not None :
            self.image = image
            self.one_d = image.reshape((-1,2))
            return
        self.image = np.zeros((self.side, self.side, 2), dtype=np.float32)
        for i in range(self.size**2) :
            image = self.readSegment(i)
            x,y = (i%self.size)*Proba.SEGMENT_SIZE, (i//self.size)*Proba.SEGMENT_SIZE
            x_len,y_len = min(Proba.SEGMENT_SIZE, self.side-x),min(Proba.SEGMENT_SIZE, self.side-y)
            self.image[y:y+y_len, x:x+x_len] = image[0:y_len, 0:x_len]
        self.one_d = self.image.reshape((-1,2))

    def setValuesOneD(self, id, value1, value2) :
        self.one_d[id] = np.array([value1,value2], dtype=np.float32)

    def addValuesOneD(self, id, value1, value2) :
        self.one_d[id] += np.array([value1,value2], dtype=np.float32)
        #x,y = id%self.side, id//self.side
        #self.image[y,x] += np.array([value1,value2,0], dtype=np.float32)

    def readValuesOneD(self, id) :
        #x,y = id%self.side, id//self.side
        #return self.image[y, x, :2]
        return self.one_d[id]

    def readValues(self, key) :
        id = Proba.getIdCards(Table.initFromKey(key)) if type(key) is str else key
        x,y = id%self.side, id//self.side
        seg_id = x//Proba.SEGMENT_SIZE + (y//Proba.SEGMENT_SIZE)*self.size
        image = self.readSegment(seg_id)
        x_mod, y_mod = x%Proba.SEGMENT_SIZE, y%Proba.SEGMENT_SIZE
        return image[y_mod, x_mod, :2]
        
    def updateValues(self, key, a, b) :
        if self.images is not None :
            id = Proba.getIdCards(Table.initFromKey(key)) if type(key) is str else key
            x,y = id%self.side, id//self.side
            seg_id = x//Proba.SEGMENT_SIZE + (y//Proba.SEGMENT_SIZE)*self.size
            x_mod, y_mod = x%Proba.SEGMENT_SIZE, y%Proba.SEGMENT_SIZE
            self.images[seg_id][y_mod, x_mod, 0] = a
            self.images[seg_id][y_mod, x_mod, 1] = b
        else :
            print("Image not loaded, writing not possible !")
            raise

    def addValues(self, key, value1, value2) :
        if self.images is not None :
            id = Proba.getIdCards(Table.initFromKey(key)) if type(key) is str else key
            x,y = id%self.side, id//self.side
            seg_id = x//Proba.SEGMENT_SIZE + (y//Proba.SEGMENT_SIZE)*self.size
            x_mod, y_mod = x%Proba.SEGMENT_SIZE, y%Proba.SEGMENT_SIZE
            self.images[seg_id][y_mod, x_mod, 0] += value1
            self.images[seg_id][y_mod, x_mod, 1] += value2
            
        else :
            print("Image not loaded, writing not possible !")
            raise

    def exportWhole(self) :
        if self.images is not None :
            image = np.zeros(shape=(self.size*self.SEGMENT_SIZE, self.size*self.SEGMENT_SIZE, 2), dtype=np.float32)
            for seg_id in range(self.size**2) :
                sub_img = self.readSegment(seg_id)
                x,y = sub_img%self.size, sub_img//self.size
                image[y:y+Proba.SEGMENT_SIZE, x:x+Proba.SEGMENT_SIZE] = sub_img
            #cv2.imwrite(self.path+"/WHOLE.png", image)
            pyexr.write(self.path+"/WHOLE.exr", {'won': image[:,:,0], 'played': image[:,:,1]})


    def writeSegments(self) :
        if self.image is not None :
            self.image = self.one_d.reshape((self.side, self.side, 2))
            self.loadSegments(self.image)
        if self.images is not None :
            for i in range(len(self.images)) :
                self.writeSegment(i, self.images[i])
        else :
            print("Image not loaded, writing not possible !")
            raise
        
    def writeSegment(self, seg_id, sub_img) :
        #print(f"{self._path}/{seg_id}.exr", sub_img.shape)
        #print(seg_id, sub_img.path)
        pyexr.write(f"{self._path}/{seg_id}.exr", {"won": sub_img[:,:,0], "played": sub_img[:,:,1]})
        
    def loadSegments(self, image = None) :
        images = np.zeros(shape=(self.size**2, Proba.SEGMENT_SIZE, Proba.SEGMENT_SIZE, 2), dtype=np.float32)
        for i in range(self.size**2) :
            if image is None :
                images[i, 0:Proba.SEGMENT_SIZE,0:Proba.SEGMENT_SIZE] = self.readSegment(i)
                #print(images[i].shape)
            elif self.side == image.shape[0] or self.size*self.SEGMENT_SIZE == image.shape[0] :
                x,y = (i%self.size)*Proba.SEGMENT_SIZE, (i//self.size)*Proba.SEGMENT_SIZE
                x_len,y_len = min(Proba.SEGMENT_SIZE, self.side-x),min(Proba.SEGMENT_SIZE, self.side-y)
                images[i, 0:y_len,0:x_len] = image[y:y+y_len, x:x+x_len]
            else :
                print("Wrong image trying to be loaded or wrong path")
                raise
        self.images = images

    def unloadSegments(self) :
        self.images = None
        
    def readSegment(self, seg_id) :
        if self.images is not None :
            return self.images[seg_id]
        
        image_data = pyexr.read(f"{self._path}/{seg_id}.exr", channels=['won', 'played'])
        return np.dstack([image_data["won"], image_data["played"]])
        #return cv2.imread(f"{self._path}/{seg_id}.exr", cv2.IMREAD_UNCHANGED)
    
    def loadBlankWhole(self) :
        self.image = np.zeros(shape=(self.side, self.side, 2), dtype=np.float32)
        self.one_d = self.image.reshape((-1,2))

    def loadBlankSegments(self) :
        self.images = np.zeros(shape=(self.size**2, Proba.SEGMENT_SIZE, Proba.SEGMENT_SIZE, 2), dtype=np.float32)
    #Static Functions
    two_cards = [0, 50, 99, 147, 194, 240, 285, 329, 372, 414, 455, 495, 534, 572, 609, 645, 680, 714, 747, 779, 810, 840, 869, 897, 924, 950, 975, 999, 1022, 1044, 1065, 1085, 1104, 1122, 1139, 1155,1170, 1184, 1197, 1209, 1220, 1230, 1239, 1247, 1254, 1260, 1265, 1269, 1272, 1274, 1275]
    three_cards = [0, 1225, 2401, 3529, 4610, 5645, 6635, 7581, 8484, 9345, 10165, 10945, 11686, 12389, 13055, 13685, 14280, 14841, 15369, 15865, 16330, 16765, 17171, 17549, 17900, 18225, 18525, 18801, 19054, 19285, 19495, 19685, 19856, 20009, 20145, 20265, 20370, 20461, 20539, 20605, 20660, 20705, 20741, 20769, 20790, 20805, 20815, 20821, 20824, 20825]
    four_cards = [0, 19600, 38024, 55320, 71535, 86715, 100905, 114149, 126490, 137970, 148630, 158510, 167649, 176085, 183855, 190995, 197540, 203524, 208980, 213940, 218435, 222495, 226149, 229425, 232350, 234950, 237250, 239274, 241045, 242585, 243915, 245055, 246024, 246840, 247520, 248080, 248535, 248899, 249185, 249405, 249570, 249690, 249774, 249830, 249865, 249885, 249895, 249899, 249900]     
    five_cards = [0, 230300, 442176, 636756, 815121, 978306, 1127301, 1263052, 1386462, 1498392, 1599662, 1691052, 1773303, 1847118, 1913163, 1972068, 2024428, 2070804, 2111724, 2147684, 2179149, 2206554, 2230305, 2250780, 2268330, 2283280, 2295930, 2306556, 2315411, 2322726, 2328711, 2333556, 2337432, 2340492, 2342872, 2344692, 2346057, 2347058, 2347773, 2348268, 2348598, 2348808, 2348934, 2349004, 2349039, 2349054, 2349059, 2349060]
    six_cards = [0, 2118760, 4025644, 5737948, 7271887, 8642641, 9864400, 10950408, 11913006, 12763674, 13513072, 14171080, 14746837, 15248779, 15684676, 16061668, 16386300, 16664556, 16901892, 17103268, 17273179, 17415685, 17534440, 17632720, 17713450, 17779230, 17832360, 17874864, 17908513, 17934847, 17955196, 17970700, 17982328, 17990896, 17997084, 18001452, 18004455, 18006457, 18007744, 18008536, 18008998, 18009250, 18009376, 18009432, 18009453, 18009459, 18009460]
    seven_cards = [0, 15890700, 29874516, 42146028, 52883601, 62250420, 70395480, 77454532, 83550986, 88796772, 93293160, 97131540, 100394163, 103154844, 105479628, 107427420, 109050580, 110395484, 111503052, 112409244, 113145525, 113739300, 114214320, 114591060, 114887070, 115117300, 115294400, 115428996, 115529943, 115604556, 115658820, 115697580, 115724712, 115743276, 115755652, 115763660, 115768665, 115771668, 115773384, 115774308, 115774770, 115774980, 115775064, 115775092, 115775099, 115775100]
    
    @staticmethod
    def createTableSevenCards() :
        table = [0]
        l_value = None
        for c in range(0, 52) :
            for b in range(c+1, 52) :
                for a in range(b+1, 52) :
                    for l in range(a+1, 52) :
                        for k in range(l+1, 52) :
                            for i in range(k+1, 52) :
                                for j in range(i+1, 52) :
                                    if b == 46 and a == 47 and l == 48 and k == 49 and i == 50 and j == 51 :
                                        l_value = Proba.getIdCards([Card(b//4,b%4), Card(a//4,a%4), Card(l//4,l%4), Card(k//4,k%4), Card(i//4,i%4), Card(j//4,j%4)])
                                    elif l_value is not None :
                                        table.append(l_value-Proba.getIdCards([Card(b//4,b%4), Card(a//4,a%4), Card(l//4,l%4), Card(k//4,k%4), Card(i//4,i%4), Card(j//4,j%4)])+table[-1]+1)
                                        l_value = None
        table.append(1+table[-1])
        print(table)
        print(len(table))

    cards_step = [two_cards, three_cards, four_cards, five_cards, six_cards, seven_cards]
    min_cards = [Card(0,1), Card(0,2), Card(0,3), Card(1, 0), Card(1, 1), Card(1, 2)]

    @staticmethod
    def getIdFromKey(key) :
        return Proba.getIdCards(Table.initFromKey(key))
    
    @staticmethod
    def getId1Cards(cards) :
        return cards[0].rank*4+cards[0].suit

    @staticmethod
    def getId2Cards(cards) :
        return Proba.two_cards[cards[0].rank*4+cards[0].suit]+cards[1].rank*4+cards[1].suit-1
    
    @staticmethod
    def getId3Cards(cards) :
        return Proba.three_cards[cards[0].rank*4+cards[0].suit]+Proba.two_cards[cards[1].rank*4+cards[1].suit]+cards[2].rank*4+cards[2].suit-52
    
    @staticmethod
    def getId4Cards(cards) :
        return Proba.four_cards[cards[0].rank*4+cards[0].suit]+Proba.three_cards[cards[1].rank*4+cards[1].suit]+Proba.two_cards[cards[2].rank*4+cards[2].suit]+cards[3].rank*4+cards[3].suit-1327
    
    @staticmethod
    def getId5Cards(cards) :
        return Proba.five_cards[cards[0].rank*4+cards[0].suit]+Proba.four_cards[cards[1].rank*4+cards[1].suit]+Proba.three_cards[cards[2].rank*4+cards[2].suit]+Proba.two_cards[cards[3].rank*4+cards[3].suit]+cards[4].rank*4+cards[4].suit-22152
    
    @staticmethod
    def getId6Cards(cards) :
        return Proba.six_cards[cards[0].rank*4+cards[0].suit]+Proba.five_cards[cards[1].rank*4+cards[1].suit]+Proba.four_cards[cards[2].rank*4+cards[2].suit]+Proba.three_cards[cards[3].rank*4+cards[3].suit]+Proba.two_cards[cards[4].rank*4+cards[4].suit]+cards[5].rank*4+cards[5].suit-272052
    
    @staticmethod
    def getId7Cards(cards) :
        return Proba.seven_cards[cards[0].rank*4+cards[0].suit]+Proba.six_cards[cards[1].rank*4+cards[1].suit]+Proba.five_cards[cards[2].rank*4+cards[2].suit]+Proba.four_cards[cards[3].rank*4+cards[3].suit]+Proba.three_cards[cards[4].rank*4+cards[4].suit]+Proba.two_cards[cards[5].rank*4+cards[5].suit]+cards[6].rank*4+cards[6].suit-2621112

    @staticmethod
    def getIdCards(cards) :
        cards = sorted(cards, key=lambda card: (card.rank, card.suit))
        match len(cards) :
            case 1 :
                return Proba.getId1Cards(cards)
            case 2 :
                return Proba.getId2Cards(cards)
            case 3 :
                return Proba.getId3Cards(cards)
            case 4 :
                return Proba.getId4Cards(cards)
            case 5 :
                return Proba.getId5Cards(cards)
            case 6 :
                return Proba.getId6Cards(cards)
            case 7 :
                return Proba.getId7Cards(cards)
    @staticmethod
    def createExrFromDict(path) :
        dict = loadDictFromFile(path)
        return Proba.convertDictToExr(dict)

    #Returns a numpy array representing the data
    @staticmethod
    def convertDictToexr(dict) :
        side = int(np.sqrt(len(dict)))+1
        image = np.zeros(shape=(side, side, 2), dtype=np.float32)

        i = 0
        for key, value in dict.items():
            if i%10000 == 0 :
                print(i/len(dict)*100, end="\r")
            if type(value) is list :
                id = Proba.getIdFromKey(key)
                x,y = id%side, id//side
                a,b = int(value[0]), int(value[1])
                image[y, x, 0] = a 
                image[y, x, 1] = b
            i+=1

        return image
    
    @staticmethod
    def loadOrSetupBlank(path, data_length) :
        size = int(np.sqrt(data_length))+1
        final_path = path+"_"+str(size)
        if os.path.exists(final_path) :
            return Proba(final_path)
        else :
            return Proba.setupBlank(path, data_length)
    
    @staticmethod
    def setupBlank(folder_path, data_length) :
        size = int(np.sqrt(data_length))+1
        final_path = folder_path+"_"+str(size)
        os.makedirs(final_path)
        proba = Proba(final_path, loadSegments=False, loadWhole=False)
        proba.loadBlankWhole()
        proba.writeSegments()
        return proba

if __name__ == "__main__" :
    path = f"D:/Poker Project/Project/Data/river_{2}.json"
    """image = Proba.createExrFromDict(path)
    cv2.imwrite(path.replace(".json", ".exr"), image)
    id = Proba.getIdFromKey("3h-2c-As-Qd-5h-7h")
    image = cv2.imread(path.replace(".json", ".exr"), cv2.IMREAD_UNCHANGED)
    side = image.shape[0]
    x,y = id//side, id%side
    print(image[x,y])"""

    #Proba.createTableSevenCards()
    
    l_id = 0
    for c in range(0, 1) :
        for b in range(c+1, 2) :
            for a in range(b+1, 3) :
                for l in range(a+1, 4) :
                    for k in range(l+1, 5) :
                        for i in range(0, 52) :
                            for j in range(i+1, 52) :
                                id = Proba.getIdCards([Card(i//4,i%4), Card(j//4,j%4)])
                                if id % 10000 == 0 :
                                    print(id, end="\r")
                                if id != l_id + 1 :
                                    print("ERROR :", id, "!=", l_id)
                                l_id = id

    """image = Proba.createPngFromDict(path)
    proba = Proba(path)
    proba.writeSegments(destination_folder, nb_segments)
    proba = Proba.fromSegments(folder)

    current_time = time.time()
    loadDictFromFile(path)
    print(f"{time.time()-current_time}s")"""

    """current_time = time.time()
    id = Proba.getIdFromKey("3h-2c-As-Qd-5h-7h")
    image = cv2.imread(path.replace(".json", ".png"), cv2.IMREAD_UNCHANGED)
    side = image.shape[0]
    x,y = id//side, id%side
    print(image[x,y])
    print(f"{time.time()-current_time}s")"""