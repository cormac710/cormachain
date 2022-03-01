import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from blockchain.block import Block
from exceptions.blockchain_validation_exceptions import BlockChainReplacementException
from wallet.transaction import Transaction

# TODO: as env variables
subscribe_key = 'sub-c-e66947e8-1bcb-11ec-a975-faf056e3304c'
publish_key = 'pub-c-11d3331a-b50d-46fc-ae46-2c63043cb4c7'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):

    def __init__(self, cormachain, transaction_pool):
        self.cormachain = cormachain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_obj):
        print(f'Channel --> {message_obj.channel} is saying {message_obj.message}')
        if message_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_obj.message)
            print('-----')
            print(self.cormachain.chain)
            print('-----')
            potential_chain = self.cormachain.chain[:]
            potential_chain.append(block)
            try:
                self.cormachain.replace_chain(potential_chain)
                self.transaction_pool.clear_transactions(self.cormachain)
                print('Chain replaced successfully')
            except BlockChainReplacementException as e:
                print(f'Chain not replaced: {e}')
        elif message_obj.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_obj.message)
            self.transaction_pool.set_transaction(transaction)
            print(' -- Transaction set -- ')



class PubSub():
    """
    Handles publish/subscribe allowing communication between nodes
    """

    def __init__(self, cormachain, transaction_pool):
        self.pubnub = PubNub(self.__configure_pub_nub())
        self.pubnub.subscribe()\
            .channels(CHANNELS.values())\
            .execute()
        self.pubnub.add_listener(Listener(cormachain, transaction_pool))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

    def __configure_pub_nub(self):
        pnConf = PNConfiguration()
        pnConf.subscribe_key = subscribe_key
        pnConf.publish_key = publish_key
        return pnConf

# if __name__ == '__main__':
    # pubsub = PubSub()
    # time.sleep(1)
    # pubsub.publish(CHANNELS['TEST'], {'message': 'hello new'})
