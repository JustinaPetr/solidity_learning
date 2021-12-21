from brownie import accounts, SimpleStorage, network

def deploy_simple_project():
    account  = accounts.load("freecodecamp-account")
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(15, {"frome": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()

    print(account)


def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    print("Hello")