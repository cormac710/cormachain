import config

from blockchain.block import Block
from exceptions.blockchain_validation_exceptions import GenesisBlockValidationException, BlockChainReplacementException
from exceptions.blockchain import BlockChainException
from wallet.transaction import Transaction
from wallet.wallet import Wallet


class Cormachain:
    """
    Blockchain: ledger to store all transactions
    Stores all blocks in the chain
    """

    def __init__(self):
        # Always need a genesis block when creating a blockchain
        self.chain = [Block.genesis_block()]

    def add_block(self, data):
        self.chain.append(
            Block.mine(self.chain[-1], data)
        )

    def replace_chain(self, incoming_chain):
        """
         - incoming must be longer than local
         - chain must be formatted correctly
        """
        if len(incoming_chain) <= len(self.chain):
            raise BlockChainReplacementException('Incoming chain must be longer than the one it is to replace')

        try:
            Cormachain.is_valid_chain(incoming_chain)
        except BlockChainException as e:
            raise BlockChainReplacementException(f'Incoming chain is incorrectly formatted due to Exception: {e}')

        self.chain = incoming_chain

    def to_json(self):
        return list(
            map(lambda block: block.to_json(), self.chain)
        )

    @staticmethod
    def from_json(chain_as_json):
        cormachain = Cormachain
        cormachain.chain = list(
            map(lambda chain_to_convert: Block.from_json(chain_to_convert), chain_as_json)
        )
        return cormachain

    @property
    def get_last_block(self):
        return self.chain[-1]

    @staticmethod
    def is_valid_chain(chain_to_validate):
        """
         Validates the chain
          - Must stat with a genesis block
          - block formatting is correct
        """
        if chain_to_validate[0] != Block.genesis_block():
            raise GenesisBlockValidationException
        for i in range(1, len(chain_to_validate)):
            block = chain_to_validate[i]
            last_block = chain_to_validate[i - 1]
            Block.is_valid_block(last_block, block)

        Cormachain.is_valid_transaction_chain(chain_to_validate)

    @staticmethod
    def is_valid_transaction_chain(chain):
        # each transaction must only appear once in the chain (unique)
        # only 1 mining reward per block
        # Each transaction must be valid
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transactin_json in block.data:
                transaction = Transaction.from_json(transactin_json)



                if transaction.id in transaction_ids:
                    raise Exception(f'transaction {transaction.id} already exists')

                transaction_ids.add(transaction.id)

                if transaction.input == config.MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('more than only one mining rewards in block'
                                        f'check block with has {block.block_hash}')
                    has_mining_reward = True
                else:
                    historic_blockchain = Cormachain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calc_balance(historic_blockchain, transaction.input['address'])
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')

                Transaction.is_valid_transaction(transaction)


    def __repr__(self):
        return f'Cormachain: {self.chain}'
