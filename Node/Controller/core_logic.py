from vote import Vote
from helper import bin2hex, hex2bin, hash_block, hash_str

import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

MINING_REWARD = 1
MAX_NONCE = 2 ** 32
MINING_DIFF = 4 # nonce start with n zeros
import random

def gen_id():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
        'private_key': private_key.exportKey(format='DER').hex(),
        'public_key': public_key.exportKey(format='DER').hex()
    }
    return response

def verify_transaction_signature(public_address, signature, transaction_dict):
    """
    Check that the provided signature corresponds to transaction
    signed by the public key (sender_address)
    """
    try:
        public_key = RSA.importKey(hex2bin(public_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction_dict).encode('utf8'))
        return verifier.verify(h, hex2bin(signature))
    except:
        return False


def submit_transaction(ToBC, voter_address, voteTo, signature, miner_address = None, token = None):
    """
    Add a transaction to curr_session array if the signature verified
    """
    transaction_dict = Vote(voter_address, voteTo, miner_address, token).to_dict()
    transaction_verification = verify_transaction_signature(
        voter_address, signature, transaction_dict)
    if transaction_verification:
        ToBC.curr_session.append(transaction_dict)
        return len(ToBC.chain) + 1
    return -1


def POW_valid(last_block, latest_session, nonce, difficulty_bits, target):
    last_hash = hash_block(last_block)
    header = str(latest_session) + str(last_hash)
    hash_rslt = hash_str(header + str(nonce))
    return hash_rslt[0:difficulty_bits:1] == target


def mine(inBC, with_difficulty_bits=MINING_DIFF):
    random.seed()
    nonce = 0
    last_block = None
    while True:
        nonce = random.randint(0, MAX_NONCE)
        last_block = inBC.chain[-1]
        target = '0' * with_difficulty_bits
        if POW_valid(last_block, inBC.curr_session, nonce, with_difficulty_bits, target):
            break
    # need to add fileds to let miner input his identity
    # submit_transaction(inBC, None, None, )
    inBC.create_block(nonce, hash_block(last_block))
