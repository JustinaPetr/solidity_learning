from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os


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
chain_id = 1337
address = "0x7AafCa0FeaDb0d3a17c25eA4933d99660a2C567e"


# create a contract with python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(address)

transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": address, "nonce": nonce,})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = os.getenv("PRIVATE_KEY"))

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# working with the contract

simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

# calling a view function


store_transaction = simple_storage.functions.store(15).buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": address, "nonce": nonce + 1,})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = os.getenv("PRIVATE_KEY"))
tx_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_store_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)