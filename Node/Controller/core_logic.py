from vote import Vote
from helper import bin2hex, hex2bin, hash_block, hash_str, dump2file

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
    pri_k_exp = private_key.exportKey(format='DER').hex()
    pub_k_exp = public_key.exportKey(format='DER').hex()
    dump2file(pri_k_exp, "pri.der")
    dump2file(pub_k_exp, "pub.der")
    response = {
        'private_key': pri_k_exp,
        'public_key': pub_k_exp
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

def verify_and_append_transaction(forBC, withTranscation):
    pass

def POW_valid(last_block, latest_session, nonce, difficulty_bits, target):
    last_hash = hash_block(last_block)
    header = str(latest_session) + str(last_hash)
    hash_rslt = hash_str(header + str(nonce))
    return hash_rslt[0:difficulty_bits:1] == target

def sign_transaction(trans_dict, with_k):
    """
    Sign transaction with private key
    """
    key = RSA.importKey(hex2bin(with_k))
    cipher = PKCS1_v1_5.new(key)
    h = SHA.new(str(trans_dict).encode('utf8'))
    return cipher.sign(h).hex()

def mine(inBC,  miner_pub_address, miner_pri_address, with_difficulty_bits=MINING_DIFF):
    global MINING_REWARD
    random.seed()
    nonce = 0
    last_block = None
    while True:
        nonce = random.randint(0, MAX_NONCE)
        last_block = inBC.chain[-1]
        target = '0' * with_difficulty_bits
        if POW_valid(last_block, inBC.curr_session, nonce, with_difficulty_bits, target):
            break
    miners_reward = Vote(None, None, miner_pub_address, MINING_REWARD).to_dict()
    inBC.submit_transaction(None, None, sign_transaction(miners_reward, miner_pri_address), miner_pub_address, MINING_REWARD)
    inBC.create_block(nonce, hash_block(last_block))
