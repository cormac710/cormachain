import os
import random
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

from blockchain.cormachain import Cormachain
from exceptions.blockchain_validation_exceptions import BlockChainReplacementException
from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet

from pubsub import PubSub


ROOT_PORT = 5000
PORT = ROOT_PORT

app = Flask(__name__)
# Allow from out local react page
# CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})
CORS(app, resources={r'/*': {'origins': 'http://127.0.0.1:3000'}})
cormachain = Cormachain()
transaction_pool  = TransactionPool()
wallet = Wallet(cormachain)
pubsub = PubSub(cormachain, transaction_pool)


@app.route('/blockchain')
def get_chain():
    return jsonify(
        cormachain.to_json()
    )


@app.route('/blockchain/range')
def get_chain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(cormachain.to_json()[::-1][start:end])


@app.route('/blockchain/length')
def get_cormachain_length():
    return jsonify(len(cormachain.to_json()))


@app.route('/blockchain/mine')
def mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(
        Transaction.reward_transaction(wallet).to_json()
    )

    cormachain.add_block(transaction_data)

    block = cormachain.get_last_block
    pubsub.broadcast_block(block)
    transaction_pool.clear_transactions(cormachain)

    return jsonify(
        block.to_json()
    )


@app.route('/wallet/transact', methods=['POST'])
def wallet_transaction():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(wallet, transaction_data['receiver'], transaction_data['amount'])
    else:
        transaction = Transaction(wallet, transaction_data['receiver'], transaction_data['amount'])

    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def wallet_info():
    return jsonify({
        'address': wallet.address,
        'balance': wallet.balance
    })


@app.route('/known-addresses')
def get_known_addresses():
    known_addresses = set()
    for block in cormachain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())
    return jsonify(
        list(known_addresses)
    )


@app.route('/transactions')
def get_transactions():
    return jsonify(
        transaction_pool.transaction_data()
    )


if os.environ.get('PEER') == 'true':
    PORT = random.randint(5001, 6000)

    full_chain = requests.get(f'http://127.0.0.1:{ROOT_PORT}/blockchain')
    print(full_chain)
    converted_chain = Cormachain.from_json(full_chain.json())
    try:
        cormachain.replace_chain(converted_chain.chain)
    except BlockChainReplacementException as ex:
        print(f"ERROR: syncing --> {ex}")

if os.environ.get('SEED') == 'True':
    for i in range(10):
        cormachain.add_block([
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json()
        ])

    for i in range(3):
        transaction_pool.set_transaction(
            Transaction(
                Wallet(), Wallet().address, random.randint(2, 50)
            )
        )

# PEER nodes must first run: # export PEER=True
print(f'Starting at port {PORT}')
app.run(host='localhost', port=PORT)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=PORT)
