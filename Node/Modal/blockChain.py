from vote import Vote

from uuid import uuid4
from time import time


MINING_REWARD = 1
MINING_DIFFICULTY = 2


class Blockchain:
    # Basic
    def __init__(self):
        self.curr_session = []
        self.chain = []
        self.nodes = set()
        self.node_id = uuid4().hex
        # init block
        self.create_block(0, '00')

    def __str__(self):
        rslt = "Node's id:"
        rslt += self.node_id
        rslt += '\n'
        for block in self.chain:
            rslt += str(block)
            rslt += '\n'
            rslt += '-->'
        return rslt

    def create_block(self, nonce, previous_hash):
        """
        Add a block of curr_session to the blockchain
        """
        block = {'block_number': len(self.chain) + 1,
                 'timestamp': time(),
                 # caveat: array in a dict is a pointer like thing
                 'history': self.curr_session.copy(),
                 'nonce': nonce,
                 'previous_hash': previous_hash}

        # Reset the current session
        self.curr_session = []

        self.chain.append(block)
        return block

    # # Submission and verification
    # def verify_transaction_signature(self, public_address, signature, transaction):
    #     """
    #     Check that the provided signature corresponds to transaction
    #     signed by the public key (sender_address)
    #     """
    #     try:
    #         public_key = RSA.importKey(hex2bin(public_address))
    #         verifier = PKCS1_v1_5.new(public_key)
    #         h = SHA.new(str(transaction).encode('utf8'))
    #         return verifier.verify(h, hex2bin(signature))
    #     except:
    #         return False

    # def reward_miners(self, miners_address):
    #     transaction = Vote(None, None, miners_address, MINING_REWARD)
    #     self.curr_session.append(transaction.to_dict())

    # def submit_transaction(self, voter_address, voteTo, signature):
    #     """
    #     Add a transaction to curr_session array if the signature verified
    #     """
    #     transaction = Vote(voter_address, voteTo, None, None).to_dict()
    #     transaction_verification = self.verify_transaction_signature(
    #         voter_address, signature, transaction)
    #     if transaction_verification:
    #         self.curr_session.append(transaction)
    #         return len(self.chain) + 1
    #     return -1


