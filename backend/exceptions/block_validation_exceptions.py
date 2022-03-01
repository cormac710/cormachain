from exceptions.blockchain import BlockChainException

class BlockValidationException(BlockChainException):
    def __init__(self, message):
        super().__init__(message)

class LastHashNotMatchingException(BlockValidationException):
    def __init__(self):
        super().__init__('The blocks last_hash must match the last blocks hash')

class ProofOfWorkNotMetException(BlockValidationException):
    def __init__(self):
        super().__init__('Proof of work must be completed')

class DifficultyIncreasedMoreThanOneException(BlockValidationException):
    def __init__(self):
        super().__init__('Difficulty must only be changed by 1')

class BlockHashException(BlockValidationException):
    def __init__(self):
        super().__init__('Block hash is not a combination of all expected fields')
