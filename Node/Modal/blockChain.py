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


