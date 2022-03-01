import time
import uuid

from wallet.wallet import Wallet
import config

class Transaction:
    """
    Tracks exchanges between sender to recipient
    """

    def __init__(self, send_wallet=None, recipient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.__create_output(send_wallet, recipient, amount)
        self.input = input or self.__create_input(send_wallet, self.output)

    def update(self, sender_wallet, receiver, amount):
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if receiver in self.output:
            self.output[receiver] = self.output[receiver] + amount
        else:
            self.output[receiver] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        # output has changed so we need to re-sign
        self.input = self.__create_input(sender_wallet, self.output)

    def to_json(self):
        # signature is byte string
        # public key is object
        return self.__dict__

    @staticmethod
    def from_json(transaction_json_repr):
        return Transaction(**transaction_json_repr)

    def __create_input(self, send_wallet, output):
        """
        structures input data for transaction and sign transaction
        """
        return {
            'timestamp': time.time_ns(),
            'amount': send_wallet.balance,
            'address': send_wallet.address,
            'public_key': send_wallet.public_key,
            'signature': send_wallet.sign(output)
        }

    def __create_output(self, send_wallet, recipient, amount):
        """
        structures output data for transaction
        """
        if amount > send_wallet.balance:
            raise Exception('Amount exceeds balance')
        # Could be formatted nicer
        #  { sender: {address: 'b8fcc814', balance '800'}, receivers: {'receiver1': '100', 'receiver2': '100'}}
        output = {}
        output[recipient] = amount
        output[send_wallet.address] = send_wallet.balance - amount

        return output

    @staticmethod
    def is_valid_transaction(transaction):
        # is transaction presenting itself as a reward
        if transaction.input == config.MINING_REWARD_INPUT:
            # to validate
            # 1) output only consists of single entry
            # 2) entry equal to reward value
            if list(transaction.output.values()) != [config.MINING_REWARD]:
                raise Exception('invalid mining reward')
            return

        total_output = sum(transaction.output.values())

        if transaction.input['amount'] != total_output:
            raise Exception('Invalid transaction')

        if not Wallet.verify_signature(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature')

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        award the miner with award transaction
        """
        output = {}
        output[miner_wallet.address] = config.MINING_REWARD
        return Transaction(input=config.MINING_REWARD_INPUT, output=output)

# if __name__ == '__main__':
#     from wallet.wallet import Wallet
#     sender_wallet = Wallet()
#     receiver = 'pat'
#     amount = 50
#     transaction = Transaction(sender_wallet, receiver, amount)
#     print(Transaction.from_json(transaction.to_json()))
# #
#     next_recipient = 'john'
#     next_amount = 75
#     transaction.update(sender_wallet, next_recipient, next_amount)
#     print(transaction.__dict__)
#     print('===')
#
#     next_amount = 25
#     transaction.update(sender_wallet, receiver, next_amount)
#     print(transaction.__dict__)
