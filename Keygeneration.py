from ART import *
import json


KeysFileName = "Keys/Ephkeys_"

for i in range(1,11):
    PairOfKeys = PrivateKeysGenerator(pow(2,i))
    DataToJson(PairOfKeys, KeysFileName+str(pow(2,i))+".json")