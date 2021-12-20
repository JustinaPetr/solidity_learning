from solcx import compile_standard, install_solc
from web3 import Web3
import json


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },

    solc_version = "0.6.0",
)

with open ("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# details for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 5777
address = "0x7AafCa0FeaDb0d3a17c25eA4933d99660a2C567e"
private_key = "0x4dfc99c8575562712a44ec4592592435e3d82078686a686d842e61bc191f6f90"

# create a contract with python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(address)

transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})
