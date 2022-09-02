import json
from web3 import Web3, HTTPProvider

blockchain_address = 'http://127.0.0.1:9545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'build/contracts/MemberKeys.json'
deployed_contract_address = '0x9cC16F5Eff8F43231A54467126C2E76e28bDc46B'
with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
MemberKeys = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

compiled_contract_path_2 = 'build/contracts/MemberKeys.json'
deployed_contract_address_2 = '0x9cC16F5Eff8F43231A54467126C2E76e28bDc46B'
with open(compiled_contract_path_2) as file:
    contract_json_2 = json.load(file)  # load contract info as JSON
    contract_abi_2 = contract_json_2['abi']  # fetch contract's abi - necessary to call its functions
TreeKeys = web3.eth.contract(address=deployed_contract_address_2, abi=contract_abi_2)


message = MemberKeys.functions.sayHello().call()
print(message)
message = TreeKeys.functions.sayHello().call()
print(message)