import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)

def verfiy_candidate_signature(public_address, signature, name):
    """
    Check that the provided signature corresponds to transaction
    signed by the public key (sender_address)
    """
    try:
        public_key = RSA.importKey(hex2bin(public_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(name).encode('utf8'))
        return verifier.verify(h, hex2bin(signature))
    except:
        return False

def gen_id():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
        'private_key': private_key.exportKey(format='DER').hex(),
        'public_key': public_key.exportKey(format='DER').hex()
    }
    return response


def sign_transaction(trans_dict, with_k):
    """
    Sign transaction with private key
    """
    key = RSA.importKey(hex2bin(with_k))
    cipher = PKCS1_v1_5.new(key)
    h = SHA.new(str(trans_dict).encode('utf8'))
    return cipher.sign(h).hex()
