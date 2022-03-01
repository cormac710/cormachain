import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature #DSS => dignital signature starter

from config import STARTING_BALANCE


class Wallet:
    """
    Wallet for a miner to track their balance and authorize transactions
    """

    def __init__(self, cormachain=None):
        self.address = str(uuid.uuid4())[0:8]
        self.cormachain = cormachain
        # SEC = Standards for Efficient Cryptography -> P = Prime -> 256 = bits
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )

        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    @property
    def balance(self):
        return Wallet.calc_balance(self.cormachain, self.address)

    def sign(self, data_to_sign):
        """Generate signature using private key"""
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data_to_sign).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())  # hashing implementation
        ))

    def serialize_public_key(self):
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify_signature(public_key, data, signature):
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())  # hashing implementation
            )
            return True
        except InvalidSignature:
            print('Invalid signature...')
            return False

    @staticmethod
    def calc_balance(cormachain, wallet_address):
        # calc balance for address considering ta within blockchain
        # bal found adding output values that belong to address since most recent transaction by
        # this address
        balance = STARTING_BALANCE
        if not cormachain:
            return balance

        for block in cormachain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == wallet_address:
                    # this means wallet is sending
                    # anytime address conducts new transaction it resets its balance
                    balance = transaction['output'][wallet_address]
                elif wallet_address in transaction['output']:
                    # This means address is receiving
                    balance += transaction['output'][wallet_address]
        return balance