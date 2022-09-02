from Crypto.Random.random import randint
from Crypto.Util import number
from cryptography.hazmat.primitives.asymmetric import ec

import json
import uuid

#NumberOfKeys = 1024*4
KEY_SIZE = 256

global P, G
P =  79836326974902925721526190392793808959860764441868273215133242786442770161241#number.getPrime(KEY_SIZE) #79836326974902925721526190392793808959860764441868273215133242786442770161241 
G = 2

def ReadPublicKeysJSON(json_object):
    first_row = list()
    for member in json_object:
        first_row.append(member['PublicEphkey'])
    return first_row

def PrivateKeysGenerator(NumberOfKeys):
    privatekeys = [None]*(NumberOfKeys)
    for i in range(0, NumberOfKeys):
        key = randint(1, int(P-1))
        #private_key = ec.generate_private_key(ec.SECP256R1())
        #key = private_key.private_numbers().private_value
        member = {
            "ID" : uuid.uuid4().hex,
            "PriveEphKey"  :key,
            "PublicEphkey" :pow(G, key, P)
        }
        privatekeys[i] = member
    return privatekeys


def TreeBasedGroupDiffieHellman(PrivateKeys, NumberOfKeys):
    Tree = list() #store the tree in an array implimentation manner
    Temp = list() #used to temporarly store diffrent level of the tree 
    LevelOfTree = NumberOfKeys
    for i in range(0, LevelOfTree, 2):
        Temp.append(pow(G,PrivateKeys[i]*PrivateKeys[1+i] ,P))
    Tree.append(Temp)
    LevelOfTree = LevelOfTree // 2
    while LevelOfTree != 1:
        T1 = Tree[-1]
        T2 = list()
        for i in range(0, LevelOfTree, 2):
            T2.append(pow(G,T1[i]*T1[1+i] ,P))
        Tree.append(T2)
        LevelOfTree = LevelOfTree // 2
    #return Tree of private keys
    Tree.reverse()
    Tree.append(PrivateKeys)
    return Tree 

def Tree_To_Array(Tree):
    tree = list()
    for level in Tree:
        for i in range(0, len(level)):
           tree.append(level[i])
    return tree 

def Get_Co_Path(position, Size, Tree):
    index = (Size -1) + position
    CoPath = list()
    if position % 2 == 0 : 
        CoPath.append(Tree[index + 1])
    else :
        CoPath.append(Tree[index - 1])

    while index != 0:
        par = (index -1 ) // 2
        if par != 0:
            if (par % 2 == 0):
                CoPath.append(Tree[par - 1])
            else :
                CoPath.append(Tree[par + 1])
        index = par
    return CoPath

def Get_parent_Path(position, Size, Tree):
    index = (Size -1) + position
    CoPath = list()
    index_of_parents = list()

    while index != 0:
        par = (index -1 ) // 2
        index = par
        CoPath.append(Tree[par])
        index_of_parents.append(index)
    return index_of_parents

def Reconstruct_root_key(Copath, privatekey):
    rootkey = -1
    for i in range(0, len(Copath)):
        rootkey = pow(Copath[i], privatekey, P)
        privatekey = rootkey
    return rootkey

def update_path_to_root_key(Copath, privatekey):
    rootkey = -1
    new_path = list()
    list_new_parents = list()
    for i in range(0, len(Copath)):
        rootkey = pow(Copath[i], privatekey, P) #private key
        new_path.append(pow(G, rootkey, P ))  # public tree
        privatekey = rootkey
    return new_path


def ReadPublicKeys(file):
    with open(file, 'r') as openfile:
      json_object = json.load(openfile)
    first_row = list()
    for member in json_object:
        first_row.append(member['PublicEphkey'])
    return first_row

def ReadPrivateKeys(file):
    with open(file, 'r') as openfile:
      json_object = json.load(openfile)
    first_row = list()
    for member in json_object:
        first_row.append(member['PriveEphKey'])
    return first_row


def LeafKeys(Publickeys, PrivateSetupKey):
    first_row = list()
    for i in range(0, len(Publickeys)):
        first_row.append(pow(Publickeys[i], PrivateSetupKey, P ))
    return first_row


def PublicTreePersiste(Tree,Suk):
    member = {
        "ID" : uuid.uuid4().hex,
        "PublicKeysofTree"  :Tree,
        "PubSetupKey" : Suk
        }
    return member

def ReadTree(file):
    with open(file, 'r') as openfile:
      json_object = json.load(openfile)
    return json_object['PublicKeysofTree'], json_object['PubSetupKey']

def Public_Tree(Tree):
    PublicTree = list()
    for i in range(0, len(Tree)):
        PublicTree.append(pow(G, Tree[i], P))  
    return PublicTree

def DataToJson(json_object, filename):
    with open(filename, "w") as outfile:
         json.dump(json_object, outfile)