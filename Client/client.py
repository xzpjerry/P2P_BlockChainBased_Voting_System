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
import sys
sys.path.append("./Modal")
sys.path.append("./View")
sys.path.append("./Controller")
from vote import Vote
from candidates import Candidates
from signer import hex2bin, sign_transaction, gen_id, verfiy_candidate_signature
from helper import restor_from_file

import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'View/templates')
sta_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'View/static')

import requests
import flask
from flask import Flask, jsonify, request, render_template

def get_candidate_public_key_from_some_secure_channel():
    # This can be done by downloading from https servers
    return '30819f300d06092a864886f70d010101050003818d0030818902818100abfac79b3656f20de2cda012482788f78a0b6e891c6b93c946c3b14617a6aa743b49a9fbbd426245b7ef8382f20c2a6f0d29ab92699961076fe38658f4e6a4bbbdededc053aa445f78a0aaf17559ee8fea17e2f19b812201c7b4a7f8029f2df8fb030561f25d8b7e9c829530633ea1cb68aed505574c34e74b2b6e20b88d20990203010001'

def get_candidate_list_from_some_secure_channel():
    # This can be done by downloading from https servers
    return Candidates()

CANDIDATES_PUBLIC_KEY = get_candidate_public_key_from_some_secure_channel()
CANDIDATES = get_candidate_list_from_some_secure_channel()

app = Flask(__name__, static_folder=sta_dir, template_folder=tmpl_dir)


@app.route('/')
def index():
    flask.g.candidates = CANDIDATES.as_list()
    return render_template('./index.html')


@app.route('/import_id')
def make_transaction():
    return render_template('./import_id.html')


@app.route('/view/transactions')
def view_transaction():
    return render_template('./view_transactions.html')

@app.route('/identity/new', methods=['GET'])
def new_identity():
    response = gen_id()
    return jsonify(response), 200


@app.route('/generate/vote', methods=['POST'])
def generate_vote():
    response = {}
    code = 200
    vote2candidate = False
    sender_address = restor_from_file("Client_pub.der")
    sender_private_key = restor_from_file("Client_pri.der")
    for candidate, sign in CANDIDATES.as_list_with_signature():
        if candidate != request.form['my_candidate']:
            continue
        if not verfiy_candidate_signature(CANDIDATES_PUBLIC_KEY, sign, candidate):
            vote2candidate = False
            break
        else:
            vote2candidate = candidate
    if not vote2candidate:
        response["error"] = "No such candidate or your candidate list is corrupted."
        code = 500
    elif not sender_address or not sender_private_key:
        response["error"] = "Please set your key-pair first"
        code = 500
    else:
        newvote = Vote(
            sender_address, vote2candidate)

        response['vote'] = newvote.to_dict()
        try:
            response['signature'] = sign_transaction(
                newvote.to_dict(), sender_private_key)
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

    # Client can only be run in local network
    # app.run(host='127.0.0.1', port=port)

    # Testing purpose
    app.run(host='0.0.0.0', port=port)
