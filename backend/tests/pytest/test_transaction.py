import pytest

from wallet.transaction import Transaction
from wallet.wallet import Wallet
import config

def test_valid_transaction():
    cormacs_wallet = Wallet()
    receiver = 'receiver'
    amount = 50
    transaction = Transaction(cormacs_wallet, receiver, amount)

    assert transaction.output[receiver] == amount
    assert transaction.output[cormacs_wallet.address] == cormacs_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == cormacs_wallet.balance
    assert transaction.input['address'] == cormacs_wallet.address
    assert transaction.input['public_key'] == cormacs_wallet.public_key

    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_invalid_transaction_exceed_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'receiver', 10000)


def test_transaction_update():
    cormac_wallet = Wallet()
    receiver = 'pat'
    amount = 50
    transaction = Transaction(cormac_wallet, receiver, amount)

    next_recipient = 'john'
    next_amount = 75
    transaction.update(cormac_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[cormac_wallet.address] == cormac_wallet.balance - amount - next_amount
    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    last_amount = 25
    transaction.update(cormac_wallet, receiver, last_amount)

    assert transaction.output[receiver] == amount + last_amount
    assert transaction.output[cormac_wallet.address] == int(cormac_wallet.balance - amount - next_amount - last_amount)
    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_is_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))


def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9001

    with pytest.raises(Exception, match='Invalid transaction'):
        Transaction.is_valid_transaction(transaction)


def test_valid_transaction_with_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)

def reward_transaction():
    miner = Wallet()
    reward_transaction = Transaction.reward_transaction(miner)

    assert reward_transaction.input == config.MINING_REWARD_INPUT
    assert reward_transaction.output[reward_transaction.address] == config.MINING_REWARD

def test_valid_reward_transaction():
    reward_transaction = Transaction.reward_transaction(Wallet())
    assert None == Transaction.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_extra_receiver():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output['extraReceiver'] = 'invalid'
    with pytest.raises(Exception, match='invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet.address] = 11111
    with pytest.raises(Exception, match='invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)