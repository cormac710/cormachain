from exceptions.blockchain import BlockChainException

class GenesisBlockValidationException(BlockChainException):
    def __init__(self):
        super().__init__('Genesis block provided is not valid...')


class BlockChainReplacementException(BlockChainException):
    def __init__(self, message):
        super().__init__(message)
