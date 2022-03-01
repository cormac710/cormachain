class TransactionPool:

    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, sender_wallet_address):
        """
        find transaction if exists based off senders wallet address
        """
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == sender_wallet_address:
                return transaction

    def transaction_data(self):
        return list(
            map(
                lambda transaction: transaction.to_json(),
                self.transaction_map.values())
        )

    def clear_transactions(self, blockchain):
        # delete blockchain recorded transactions from pool
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass
