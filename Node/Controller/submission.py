from vote import Vote

import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

def bin2hex(binStr):
    return binascii.hexlify(binStr)

def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)

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
