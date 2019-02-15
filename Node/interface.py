import sys
sys.path.append("./Modal")
sys.path.append("./View")
sys.path.append("./Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from blockChain import Blockchain
from vote import Vote
from core_logic import mine, gen_id
from helper import restor_from_file

import requests
from flask import Flask, jsonify, request, render_template, abort

# Allowing request from other server(node)
from flask_cors import CORS

# Handling path string
import os
tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'View/templates')
sta_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'View/static')

# Instantiate the Blockchain
blockchain = restor_from_file()
if not blockchain:
    blockchain = Blockchain()

MINERS_PUBLIC_ADDRESS = restor_from_file('pub.der')
MINERS_PRIVATE_ADDRESS = restor_from_file('pri.der')

import threading
MINER_WORKER = None


def from_locoal_host(request):
    ip = None
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip == '127.0.0.1'


def return_fresh_thread(arguments):
    return threading.Thread(target=mine, args=arguments)


def chain2list(blockchain, to_a_list):
    for block in blockchain.chain:
        for vote_dict in block['history']:
            to_a_list.append(vote_dict)


# Instantiate the Node
app = Flask(__name__, static_folder=sta_dir, template_folder=tmpl_dir)
CORS(app)


@app.route('/')
def index():
    if not from_locoal_host(request):
        abort(404)
    global MINER_WORKER
    global blockchain
    table_items_outstanding = []
    for vote_dict in blockchain.curr_session:
        table_items_outstanding.append(vote_dict)

    table_items_mined = []
    chain2list(blockchain, table_items_mined)

    isMining = MINER_WORKER and MINER_WORKER.isAlive()
    return render_template('./index.html', index_is="isMining", table_items_outstanding=table_items_outstanding, table_items_mined=table_items_mined, isMining=isMining)


@app.route('/mine', methods=['GET'])
def start_mining():
    if not from_locoal_host(request):
        return "How do you get here?", 404
    global MINER_WORKER
    global MINERS_PRIVATE_ADDRESS
    global MINERS_PUBLIC_ADDRESS
    response = {}
    code = 200
    if not MINERS_PUBLIC_ADDRESS or not MINERS_PRIVATE_ADDRESS:
        response['error'] = "Please set your key-pair first"
        code = 400
    elif MINER_WORKER and MINER_WORKER.isAlive():
        response['error'] = "This node is already mining."
        code = 400
    else:
        MINER_WORKER = return_fresh_thread(
            (blockchain, MINERS_PUBLIC_ADDRESS, MINERS_PRIVATE_ADDRESS))
        MINER_WORKER.start()
    return jsonify(response), code


@app.route('/configure')
def configure():
    if not from_locoal_host(request):
        abort(404)
    return render_template('./configure.html', index_is="isConfiguring")


@app.route('/import_id')
def new_id():
    if not from_locoal_host(request):
        abort(404)
    return render_template('./import_id.html', index_is="isImporting")


@app.route('/identity/new', methods=['GET'])
def new_identity():
    if not from_locoal_host(request):
        return "How do you get here", 404
    response = gen_id()
    global MINERS_PRIVATE_ADDRESS
    global MINERS_PUBLIC_ADDRESS
    MINERS_PRIVATE_ADDRESS = response.get("private_key")
    MINERS_PUBLIC_ADDRESS = response.get("public_key")
    return jsonify(response), 200

# Functions below are open to the public


@app.route('/chain', methods=['GET'])
def get_chain_records():
    response = {}
    records = []
    get_chain_records(records)
    response["chain"] = records
    return jsonify(response), 200


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    # Get transactions from transactions pool
    outstanding_rslt = blockchain.curr_session

    response = {'transactions': outstanding_rslt}
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form
    response = {}
    # Check that the required fields are in the POST'ed data
    required = ['voter_address_con', 'vote2_con', 'signature_con']
    if not all(k in values for k in required):
        response['error'] = 'Missing values'
        return jsonify(response), 400
    # Create a new Transaction
    rslt = blockchain.submit_transaction(
        values['voter_address_con'], values['vote2_con'], values['signature_con'])

    if rslt == -1:
        response['error'] = 'Invalid Vote!'
        return jsonify(response), 400
    response = {'message': 'Transaction will be added to Block soon.'}
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    import atexit
    from helper import dump2file
    atexit.register(dump2file, blockchain)

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except KeyboardInterrupt:
        dump2file(blockchain)
