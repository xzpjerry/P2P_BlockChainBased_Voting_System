import binascii
import json
from hashlib import sha256


def bin2hex(binStr):
    return binascii.hexlify(binStr)


def hex2bin(hexStr):
    return binascii.unhexlify(hexStr).decode('utf-8')


def hash_block(block_dict):
    jsonified_block = json.dumps(block_dict).encode()
    return sha256(jsonified_block).hexdigest()


def hash_str(astr):
    return sha256(astr.encode('utf-8')).hexdigest()


import pickle


def dump2file(obj, file='BC.dat'):
    print(obj)
    with(open(file, 'wb')) as f:
        pickle.dump(obj, f)


def restor_from_file(file='BC.dat'):
    rslt = None
    try:
        with(open(file, 'rb')) as f:
            rslt = pickle.load(f)
    except:
        return None
    return rslt
