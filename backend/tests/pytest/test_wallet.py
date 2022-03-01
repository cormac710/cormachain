# changing to use pytest this time to try it out

from wallet.wallet import Wallet
from wallet.transaction import Transaction
from blockchain.cormachain import Cormachain

import config

def test_valid_signature():
    data = { 'message': 'test'}

    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify_signature(wallet.public_key, data, signature)


def test_invalid_signature():
    data = { 'message': 'test'}

    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify_signature(Wallet().public_key, data, signature)

def test_calculate_balance():
    cormacchain = Cormachain()
    cormac_wallet = Wallet(cormacchain)

    assert Wallet.calc_balance(cormacchain, cormac_wallet.address) == config.STARTING_BALANCE

    amount = 50
    t1 = Transaction(cormac_wallet, 'otherCormac', amount)
    cormacchain.add_block([t1.to_json()])
    assert Wallet.calc_balance(cormacchain, cormac_wallet.address) == config.STARTING_BALANCE - amount

    received_amt_1 = 25
    received_transaction_1 = Transaction(Wallet(), cormac_wallet.address, received_amt_1)
    received_transaction_2 = Transaction(Wallet(), cormac_wallet.address, 32)

    cormacchain.add_block([received_transaction_1.to_json(), received_transaction_2.to_json()])
    assert Wallet.calc_balance(cormacchain, cormac_wallet.address) == (config.STARTING_BALANCE - 50) \
           + received_amt_1 + 32
    assert cormac_wallet.balance == (config.STARTING_BALANCE - 50) + received_amt_1 + 32