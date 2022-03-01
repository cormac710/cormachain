import time

from unittest import TestCase

from blockchain.cormachain import Cormachain
from blockchain.block import Block
from config import MINE_RATE, SECONDS
from exceptions.block_validation_exceptions import LastHashNotMatchingException, ProofOfWorkNotMetException, \
    DifficultyIncreasedMoreThanOneException, BlockHashException
from exceptions.blockchain_validation_exceptions import GenesisBlockValidationException, BlockChainReplacementException
from util.constants import GENESIS
from util.hex_binary_converter import convert_hex_to_binary
from wallet.transaction import Transaction
from wallet.wallet import Wallet

BLOCK_NAME_ONE = 'One'
BLOCK_NAME_TWO = 'Two'
BLOCK_NAME_THREE = 'Three'


class TestCormachain(TestCase):
    # TOOD: tests can be improved but for this they are a second priority, im here to learn blockchain
    # THIS wouldnt be the case in real life or production, just for educational sake this time

    def __create_cormachain(self):
        cormachain = Cormachain()
        chain = cormachain.chain
        return chain

    def __create_cormachain_and_one_block(self):
        cormachain = Cormachain()
        cormachain.add_block(BLOCK_NAME_ONE)
        chain = cormachain.chain
        genesys = chain[0]
        block_one = chain[1]
        return block_one, genesys

    def __create_cormachain_with_three_blocks(self):
        cormacchain = Cormachain()
        for i in range(3):
            cormacchain.add_block([
                Transaction(Wallet(), 'receiver', i).to_json()
            ])
        return cormacchain

    def test_only_genesis_after_creation(self):
        created_cormachain = Cormachain()
        chain = created_cormachain.chain

        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0].last_hash, GENESIS)
        self.assertTrue(isinstance(chain[0], Block))

    def test_add_block(self):
        cormachain = self.__create_cormachain_with_three_blocks()

        chain = cormachain.chain
        block_one = chain[1]
        block_two = chain[2]

        self.assertEqual(len(chain), 4)

        self.assertEqual(block_one.data[0]['output']['receiver'], 0)
        self.assertTrue(isinstance(block_one, Block))

        self.assertEqual(block_two.data[0]['output']['receiver'], 1)
        self.assertTrue(isinstance(block_two, Block))

    def test_hash(self):
        pass

    def test_assert_quickly_mined_difficulty(self):
        last_block = Block.genesis_block()
        self.assertEqual(last_block.difficulty, 3)

        test_block = Block.mine(last_block, BLOCK_NAME_ONE)
        self.assertEqual('00', convert_hex_to_binary(test_block.block_hash)[0:test_block.difficulty])
        self.assertEqual(test_block.difficulty, 2)

    def test_assert_slowly_mined_difficulty(self):
        last_block = Block.genesis_block()
        self.assertEqual(last_block.difficulty, 3)

        time.sleep((MINE_RATE / SECONDS) + 1)

        test_block = Block.mine(last_block, BLOCK_NAME_ONE)
        self.assertEqual('00', convert_hex_to_binary(test_block.block_hash)[0:test_block.difficulty])
        self.assertEqual(test_block.difficulty, 2)

    def test_difficulty_limit_at_1(self):
        last_block = Block(time.time_ns(), 'last_hash', 'hash', 'data', 1, 0)
        self.assertEqual(last_block.difficulty, 1)
        time.sleep((MINE_RATE / SECONDS) + 1)
        self.assertEqual(last_block.difficulty, 1)

    def test_is_valid_block(self):
        block_one, genesys = self.__create_cormachain_and_one_block()

        self.assertTrue(Block.is_valid_block(genesys, block_one))

    def test_valid_block_bad_last_hash(self):
        block_one, genesys = self.__create_cormachain_and_one_block()
        block_one.last_hash = 'im hacking you'

        with self.assertRaises(LastHashNotMatchingException):
            Block.is_valid_block(genesys, block_one)

    def test_valid_block_bad_pow(self):
        block_one, genesys = self.__create_cormachain_and_one_block()
        block_one.block_hash = 'aaaa'

        with self.assertRaises(ProofOfWorkNotMetException):
            Block.is_valid_block(genesys, block_one)

    def test_valid_block_with_hacked_difficuilty(self):
        block_one, genesys = self.__create_cormachain_and_one_block()
        difficulty_change = 5
        block_one.difficulty = difficulty_change

        with self.assertRaises(DifficultyIncreasedMoreThanOneException):
            Block.is_valid_block(genesys, block_one)

    def test_valid_block_hacked_block_hash(self):
        block_one, genesys = self.__create_cormachain_and_one_block()
        block_one.block_hash = '0000aaaaaaaaaaa'

        with self.assertRaises(BlockHashException):
            Block.is_valid_block(genesys, block_one)

    def test_blockchain_three_blocks(self):
        chain = self.__create_cormachain_with_three_blocks()
        self.assertTrue(True, chain.is_valid_chain(chain.chain))

    def test_is_valid_with_bad_genesys(self):
        cormacchain = self.__create_cormachain_with_three_blocks()
        cormacchain.chain[0].block_hash = 'hacked hash'

        with self.assertRaises(GenesisBlockValidationException):
            Cormachain.is_valid_chain(cormacchain.chain)

    def test_chain_replacement(self):
        cormacchain = self.__create_cormachain_with_three_blocks()
        otherchain = Cormachain()
        otherchain.replace_chain(cormacchain.chain)

        self.assertEqual(cormacchain.chain, otherchain.chain)

    def test_chain_replacement_chain_too_small(self):
        cormacchain = self.__create_cormachain_with_three_blocks()
        otherchain = Cormachain()

        with self.assertRaises(BlockChainReplacementException):
            cormacchain.replace_chain(otherchain.chain)

    def test_chain_replacement_bad_format(self):
        cormacchain = self.__create_cormachain_with_three_blocks()
        otherchain = Cormachain()
        cormacchain.chain[2].block_hash = '0000aabb'

        with self.assertRaises(BlockChainReplacementException):
            otherchain.replace_chain(cormacchain.chain)

    def test_valid_transaction_chain(self):
        cormacchain = self.__create_cormachain_with_three_blocks()
        self.assertIsNone(Cormachain.is_valid_transaction_chain(cormacchain.chain))

    def test_is_valid_transaction_chain(self):
        cormacchain = self.__create_cormachain_with_three_blocks()

        wallet = Wallet()
        bad_transaction = Transaction(wallet, 'receiver', 1)
        bad_transaction.output[wallet.address] = 9000
        bad_transaction.input['amount'] = 9001
        bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

        cormacchain.add_block([bad_transaction.to_json()])
        with self.assertRaises(Exception) as exception_context:
            Cormachain.is_valid_transaction_chain(cormacchain.chain)
        self.assertEqual(f'Transaction {bad_transaction.id} has an invalid input amount', str(exception_context.exception))
