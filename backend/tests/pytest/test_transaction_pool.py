from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet

from blockchain.cormachain import Cormachain

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'cormac', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction

def test_clear_pool():
    pool = TransactionPool()
    transaction = Transaction(Wallet(), 'cormac', 1)
    transaction2 = Transaction(Wallet(), 'other me', 2)

    pool.set_transaction(transaction)
    pool.set_transaction(transaction2)

    cormachain = Cormachain()
    cormachain.add_block([transaction.to_json(), transaction2.to_json()])

    assert transaction.id in pool.transaction_map
    assert transaction2.id in pool.transaction_map

    pool.clear_transactions(cormachain)

    assert transaction.id not in pool.transaction_map
    assert transaction2.id not in pool.transaction_map
