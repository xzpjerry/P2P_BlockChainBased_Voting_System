import sys
sys.path.append("../Modal")
sys.path.append("../View")
sys.path.append("../Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from vote import Vote
from core_logic import verify_transaction_signature
from uuid import uuid4
from time import time
from threading import Lock

MINING_REWARD = 1
MINING_DIFFICULTY = 2

# Picle currently cannot dump lock object


class Thread_lock():
    TLock = Lock()


class Blockchain:
    # Basic
    def __init__(self):
        self.curr_session = []
        self.chain = []
        self.nodes = set()
        self.node_id = uuid4().hex
        self.create_block(0, 'Origin_Block')

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
        block = {}
        Thread_lock.TLock.acquire()
        try:
            block = {'block_number': len(self.chain) + 1,
                     'timestamp': time(),
                     # caveat: array in a dict is a pointer like thing
                     'history': self.curr_session.copy(),
                     'nonce': nonce,
                     'previous_hash': previous_hash}

            # Reset the current session
            self.curr_session = []
            self.chain.append(block)
        finally:
            Thread_lock.TLock.release()
        return block

    def submit_transaction(self, voter_address, voteTo, signature, miner_address=None, token=None):
        """
        Add a transaction to curr_session array if the signature verified
        """
        transaction_dict = Vote(voter_address, voteTo,
                                miner_address, token).to_dict()
        transaction_verification = False
        if voter_address:
            transaction_verification = verify_transaction_signature(
                voter_address, signature, transaction_dict)
        elif miner_address:
            transaction_verification = verify_transaction_signature(
                miner_address, signature, transaction_dict)
        if transaction_verification:
            Thread_lock.TLock.acquire()
            try:
                self.curr_session.append(transaction_dict)
            finally:
                Thread_lock.TLock.release()
                return len(self.chain) + 1
        return -1
