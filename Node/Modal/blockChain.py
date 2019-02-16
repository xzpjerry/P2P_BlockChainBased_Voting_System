import sys
sys.path.append("../Modal")
sys.path.append("../View")
sys.path.append("../Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from vote import Vote
from core_logic import verify_transaction_signature, POW_valid, sign_transaction
from helper import hash_block
from uuid import uuid4
from time import time
from threading import Lock
import random

# Picle currently cannot dump lock object


class Thread_lock():
    TLock = Lock()


class Blockchain:
    # Basic
    def __init__(self):
        self.MINING_REWARD = 1
        self.MINING_DIFF = 4
        self.MAX_NONCE = 2**32

        self.curr_session = []
        self.chain = []
        self.nodes = set()
        self.node_id = uuid4().hex
        self.create_block(0, '00')

    def __str__(self):
        rslt = "Node's id:"
        rslt += self.node_id
        rslt += '\n'
        rslt += "Current session:"
        rslt += str(self.curr_session)
        rslt += '\n'
        for block in self.chain:
            rslt += str(block)
            rslt += '\n'
            rslt += '-->'
        return rslt

    def is_valid(self):
        i = 1
        last_block = self.chain[0]
        # the chain might be appended with new block during the validation
        # need to call this using a worker thread
        while i < len(self.chain):
            current_block = self.chain[i]
            pre_hash = current_block.get('previous_hash')
            if not pre_hash or pre_hash != hash_block(last_block):
                return False

            records = current_block.get('history')
            if not records:
                return False
            records = records[:-1]

            nonce = current_block.get('nonce')
            if not nonce:
                return False

            mining_diff = current_block.get('mining_diff')
            if not mining_diff:
                return False
            target = '0' * mining_diff

            if not POW_valid(last_block, records, nonce, mining_diff, target):
                return False

            last_block = current_block
            i += 1
        return True

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
                     'mining_diff': self.MINING_DIFF,
                     'previous_hash': previous_hash}

            # Reset the current session
            self.curr_session = []
            self.chain.append(block)
            return block
        except:
            return None
        finally:
            Thread_lock.TLock.release()

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
                return len(self.chain) + 1
            except:
                return -1
            finally:
                Thread_lock.TLock.release()
        else:
            return -1

    def mine(self, miner_pub_address, miner_pri_address):
        random.seed()
        nonce = 0
        last_block = None
        while True:
            # Need to update the block info from peers here

            nonce = random.randint(0, self.MAX_NONCE)
            last_block = self.chain[-1]
            target = '0' * self.MINING_DIFF
            if POW_valid(last_block, self.curr_session, nonce, self.MINING_DIFF, target):
                break
        miners_reward = Vote(None, None, miner_pub_address,
                             self.MINING_REWARD).to_dict()
        self.submit_transaction(None, None, sign_transaction(
            miners_reward, miner_pri_address), miner_pub_address, self.MINING_REWARD)
        self.create_block(nonce, hash_block(last_block))
