import json
from web3 import Web3, HTTPProvider
import time
from ART import *

infura_url = "https://ropsten.infura.io/v3/0c4f533af2ff45f79d2101a05fef34bf"#"https://ropsten.infura.io/v3/00f76b272fb34ad29c2bcc24a07e1081"
web3 = Web3(Web3.HTTPProvider(infura_url))
res = web3.isConnected()
print("[!]Blockchain status : ", res)
is_address_valid = web3.isAddress('0xaE12E30AC411B1B2088F9E978f763aab4Dc245c0')
print("[!]Valide account address :", is_address_valid)
print("[!]Account Blalance : ", web3.fromWei(web3.eth.get_balance("0xaE12E30AC411B1B2088F9E978f763aab4Dc245c0"), 'ether'))
wallet_private_key   = "a7fb512e76728e763044acbc172995196cf5ce2e60433e03de4a4c55918b9a4d"
wallet_address       = "0xaE12E30AC411B1B2088F9E978f763aab4Dc245c0"

KeycontractAddress  = "0xA2DdA83c7f0C866577e168FE93F76a7a73538434"
TreecontractAddress = "0x781EDbA9D22dBfD9fC92E6fa9ab45eA46Ea476fD"


compiled_contract_path = 'build/contracts/MemberKeys.json'
deployed_contract_address = KeycontractAddress
with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
MemberKeys = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

compiled_contract_path_2 = 'build/contracts/TreeKeys.json'
deployed_contract_address_2 = TreecontractAddress
with open(compiled_contract_path_2) as file:
    contract_json_2 = json.load(file)  # load contract info as JSON
    contract_abi_2 = contract_json_2['abi']  # fetch contract's abi - necessary to call its functions
TreeKeys = web3.eth.contract(address=deployed_contract_address_2, abi=contract_abi_2)


print('*'*30)
message = MemberKeys.functions.sayHello().call()
print(message)
message = TreeKeys.functions.sayHello().call()
print(message)
print('*'*30)




keyfile = "Keys/Ephkeys_1024.json"
f = open(keyfile, 'r')
data = f.read()
records = json.loads(data)
gasprice = 40
Ids = list()
i = 0
current_nonce = web3.eth.getTransactionCount(wallet_address)
print("first nonce :",current_nonce)
for member in records:
    Ids.append(member['ID'])
    #print(member['ID'])
    '''

    if MemberKeys.functions.isRegistred(member['ID']).call() == False :
        print("Adding member N :",i )
        txn_dict = MemberKeys.functions.Register(str(member['ID']), member['PublicEphkey'],1 ).buildTransaction({
                'chainId': 3,
                'gas': 200000,
                'gasPrice': web3.toWei(str(gasprice), 'gwei'),
                'nonce': current_nonce, })
        signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
        result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        #gasprice += 2
        current_nonce += 1
    else :
        print("Already registered", i)
    i+= 1 
'''  


N = 64
TreefileName = "Trees/tree_"
#print(MemberKeys.functions.GetMemberKey(Ids, 32).call())    
PublicKeys = MemberKeys.functions.GetMemberKey(Ids, N).call()
setup = randint(1, int(P-1))
SETUP = pow(G, setup, P)
leafkeys = LeafKeys(PublicKeys, setup)
PrivateTree = TreeBasedGroupDiffieHellman(leafkeys, N)
PrivateTreeInArray = Tree_To_Array(PrivateTree)
pubtree = Public_Tree(PrivateTreeInArray)
#DataToJson(PublicTreePersiste(pubtree,SETUP ),TreefileName+str(N)+".json")

print(pubtree[0])
gasprice = 400


'''
txn_dict = TreeKeys.functions.SetArtTree("tree_"+str(N),SETUP, pubtree ).buildTransaction({
            'chainId': 3,
            'gas': 70000000,
            'gasPrice': web3.toWei(str(gasprice), 'gwei'),
            'nonce': current_nonce, })
signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
'''

print(TreeKeys.functions.GetArtTree("tree_"+str(N)).call()[0])






'''
keyfile = "Keys/Ephkeys_"
files = list()
for i in range(1,9) :
    filename= keyfile + str(pow(2,i)) + ".json"
    files.append(filename)

print(files)
'''
'''

#registring Key to the blockchain keys to test
for file in files:
    print("*"*40)
    f = open(file, 'r')
    data = f.read()
    records = json.loads(data)
    IDs = list()
    for record in records:
        if (MemberKeys.functions.isRegistred(record['ID']).call() == True):
            print("Already registred")
        else :
            MemberKeys.functions.Register(record['ID'],record['PublicEphkey'],1).transact()


'''
'''
TreefileName = "Trees/tree_"
##Retriving keys
for file in files:
    print("*"*40)
    f = open(file, 'r')
    data = f.read()
    records = json.loads(data)
    IDs = list()
    for record in records:
        IDs.append(record['ID'])
    print(len(IDs))
    start = time.time()
    PublicKeys = MemberKeys.functions.GetMemberKey(IDs, len(IDs)).call()
    ##Build ART Tree
    setup = randint(1, int(P-1))
    SETUP = pow(G, setup, P)
    leafkeys = LeafKeys(PublicKeys, setup)
    PrivateTree = TreeBasedGroupDiffieHellman(leafkeys, len(IDs))
    PrivateTreeInArray = Tree_To_Array(PrivateTree)
    pubtree = Public_Tree(PrivateTreeInArray)
    DataToJson(PublicTreePersiste(pubtree,SETUP ),TreefileName+str(len(IDs))+".json")
    end = time.time()
    TreeKeys.functions.SetArtTree(TreefileName+str(len(IDs)),SETUP, pubtree ).transact()

    print(pubtree[0])
    print("took", end-start)
'''