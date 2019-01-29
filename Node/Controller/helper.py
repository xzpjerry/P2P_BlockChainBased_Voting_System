import binascii
import json
from hashlib import sha256

def bin2hex(binStr):
    return binascii.hexlify(binStr)

def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)

def hash_block(block_dict):
	jsonified_block = json.dumps(block_dict).encode()
	return sha256(jsonified_block).hexdigest()

def hash_str(astr):
	return sha256(astr.encode('utf-8')).hexdigest()