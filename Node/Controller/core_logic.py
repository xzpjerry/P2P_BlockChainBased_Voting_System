from vote import Vote
from helper import bin2hex, hex2bin, hash_block, hash_str

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

MAX_NONCE = 2 ** 32
MINING_DIFF = 4
import random


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


def submit_transaction(ToBC, voter_address, voteTo, signature):
    """
    Add a transaction to curr_session array if the signature verified
    """
    transaction_dict = Vote(voter_address, voteTo, None, None).to_dict()
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
    inBC.create_block(nonce, hash_block(last_block))
    return True
