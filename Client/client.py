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
from signer import hex2bin, sign_transaction, gen_id

import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'View/templates')
sta_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'View/static')

import requests
import flask
from flask import Flask, jsonify, request, render_template

CANDIDATES = Candidates()

app = Flask(__name__, static_folder=sta_dir, template_folder=tmpl_dir)


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
    response = gen_id()
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
