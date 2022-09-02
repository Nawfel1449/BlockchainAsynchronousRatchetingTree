import json
from web3 import Web3, HTTPProvider
import time
from ART import *
import matplotlib.pyplot as plt

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


test= 512
KeysFileName = "Keys/Ephkeys_"
TreefileName = "Trees/tree_"
X = list()
Y = list()

current_nonce = web3.eth.getTransactionCount(wallet_address)
gasprice = 40
for i in range(1,10):
    print("*"*30)
    test = pow(2,i)
    X.append(test)
    start = time.time()

    PrivateKeys = ReadPrivateKeys(KeysFileName+str(test)+".json")
    readpubtree, readsetup   = ReadTree(TreefileName+str(test)+".json")

    i = 0
    copath = Get_Co_Path(i, test,readpubtree)
    index_of_parents = Get_parent_Path(i, test,readpubtree)
    print(index_of_parents)
    new_key = randint(1, int(P-1))
    new_pub_key = pow(G, new_key, P)
    new_parents_keys = update_path_to_root_key(copath,new_key)
    print(new_parents_keys)
    print(len(new_parents_keys))
    print("tree_"+str(test))

    print(TreeKeys.functions.GetUpdates("tree_"+str(test)).call())
    '''
    txn_dict = TreeKeys.functions.SetUpdate("tree_"+str(test), new_parents_keys, new_pub_key ).buildTransaction({
                'chainId': 3,
                'gas': 3000000,
                'gasPrice': web3.toWei(str(gasprice), 'gwei'),
                'nonce': current_nonce, })
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #gasprice += 2
    current_nonce += 1
    '''
    end = time.time()
    print("took",end-start)
    Y.append(end-start)







fig,ax=plt.subplots()
ax.plot(X, Y, 'r+-',label='B-ART')
ax.set_xlabel("Number of participants")
ax.set_ylabel("time in s")
ax.set_ylabel("Temps d'execution en S")
plt.legend()
plt.show()