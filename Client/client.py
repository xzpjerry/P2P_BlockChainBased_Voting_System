'''
title           : blockchainBased_voting_client.py
description     : A blockchain voting client implemenation, with the following features
                  - Identity generation using Public/Private key encryption (based on RSA algorithm)
                  - Generation of vote with RSA encryption      
author          : Jerry Xie
date_created    : 20190118
date_modified   : 20190118
version         : 0.1
usage           : python blockchain_client.py
python_version  : 3.6.5
Comments        : 
References      : Will fill out this part when the work is done
'''
from candidates import Candidates
from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
import flask
from flask import Flask, jsonify, request, render_template

CANDIDATES = Candidates()


class Vote:

    def __init__(self, sender_address, sender_private_key, vote):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.vote = vote

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'vote': self.vote})

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(
            binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/make/vote')
def make_transaction():
    flask.g.candidates = CANDIDATES.as_list()
    return render_template('./make_vote.html')


@app.route('/view/transactions')
def view_transaction():
    return render_template('./view_transactions.html')


@app.route('/identity/new', methods=['GET'])
def new_identity():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }

    return jsonify(response), 200


@app.route('/generate/vote', methods=['POST'])
def generate_vote():
    response = {}
    code = 200
    vote2candidate = None
    for candidate in CANDIDATES.as_list():
        if request.form.get("my_candidate") == candidate:
            vote2candidate = candidate
            break
    if not vote2candidate:
        response["error"] = "No such candidate."
        code = 500
    else:
        sender_address = request.form['sender_address']
        sender_private_key = request.form['sender_private_key']
        vote = Vote(
            sender_address, sender_private_key, vote2candidate)

        response['vote'] = vote.to_dict()
        try:
            response['signature'] = vote.sign_transaction()
        except:
            response["error"] = "The key pair does not work."
            code = 500

    return jsonify(response), code


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
