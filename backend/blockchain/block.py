import time

import config

from util.constants import GENESIS
from util.hasher import hasher
from util.hex_binary_converter import convert_hex_to_binary
from exceptions.block_validation_exceptions import LastHashNotMatchingException, ProofOfWorkNotMetException, \
    DifficultyIncreasedMoreThanOneException, BlockHashException

GENESIS_DATA = {
    'timestamp' : 1,
    'last_hash': f'{GENESIS}',
    'block_hash': f'{GENESIS}_hash',
    'data': [],
    'difficulty': 3,
    'nonce': f'{GENESIS}_nonce'
}

class Block:
    """
    Storage unit for transactions that supports crypto currency
    """
    def __init__(self, timestamp, last_hash, block_hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.block_hash = block_hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def to_json(self):
        return self.__dict__

    @staticmethod
    def genesis_block():
        return Block(**GENESIS_DATA)

    @staticmethod
    def mine(last_block, data):
        """
        mines based of the last block in the chain, until leading 0s PoW is matching
        """
        difficulty, hash, last_hash, nonce, timestamp = Block.__initialize_mine_variables(last_block)

        # check for leading 0s based of the binary representation of the hash
        while convert_hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            # keep recreating the hash until the number of 0s at the end match the difficulty
            # example for difficulty of 2 : 12n3y237cdse00
            nonce +=1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = hasher(timestamp, last_hash, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def __initialize_mine_variables(last_block):
        nonce = 0
        timestamp = time.time_ns()
        last_hash = last_block.block_hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        hash = hasher(timestamp, last_hash, difficulty, nonce)
        return difficulty, hash, last_hash, nonce, timestamp

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        calc adjusted difficulty, either increases or decreases difficulty
        """
        if (new_timestamp - last_block.timestamp) < config.MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Enforces following rules:
         - ensures block hash is a combination of block fields (proves fields werent tampered with to change in favour for an attacker)
         - must have expected last_hash reference
         - must meet proof of work
         - difficulty only adjusted by 1
        """
        if block.last_hash != last_block.block_hash:
            raise LastHashNotMatchingException

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise DifficultyIncreasedMoreThanOneException

        if convert_hex_to_binary(block.block_hash)[0:block.difficulty] != ('0' * block.difficulty):
            raise ProofOfWorkNotMetException

        reconstructed_hash = hasher(block.timestamp, block.last_hash, block.difficulty, block.nonce)
        if reconstructed_hash != block.block_hash:
            raise BlockHashException

        return True

    @staticmethod
    def from_json(block_as_json):
        return Block(**block_as_json)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'Block({self.__dict__})'
