import requests
import time


from wallet.wallet import Wallet

LOCALHOST_BASE = 'http://localhost:5000'
BLOCKCHAIN_URI = LOCALHOST_BASE + '/blockchain'
MINE_URI = BLOCKCHAIN_URI + '/mine'
WALLET_TRANSACT_URI = LOCALHOST_BASE + '/wallet/transact'

def get_blockchain():
    return requests.get(BLOCKCHAIN_URI).json()


def get_blockchain_mine():
    r = requests.get(MINE_URI)
    return r.json()


def post_wallet_transaction(receiver, amount):
    return requests.post(
        WALLET_TRANSACT_URI,
        json={ 'receiver': receiver, 'amount': amount }
    ).json()

def get_wallet_info():
    return requests.get(
        LOCALHOST_BASE + '/wallet/info'
    ).json()

start_blockchain = get_blockchain()
print(f'started --> {start_blockchain}')

receiver_one = Wallet().address

post_wallet_transaction_one = post_wallet_transaction(receiver_one, 30)
print(f'post_wallet_transaction_one --> {post_wallet_transaction_one}')
time.sleep(1)
post_wallet_transaction_two = post_wallet_transaction(receiver_one, 44)
print(f'post_wallet_transaction_two --> {post_wallet_transaction_two}')

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'mined --> {mined_block}')

wallet_info = get_wallet_info()
print(f'Wallet info: {wallet_info}')
