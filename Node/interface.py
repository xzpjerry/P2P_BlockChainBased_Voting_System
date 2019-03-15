import sys
sys.path.append("./Modal")
sys.path.append("./View")
sys.path.append("./Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from time import ctime
from blockChain import Blockchain
from vote import Vote
from core_logic import gen_id, verify_object_signature
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
blockchain.curr_session = []
blockchain.update_chain_from_nodes()

MINERS_PUBLIC_ADDRESS = restor_from_file('pub.der')
MINERS_PRIVATE_ADDRESS = restor_from_file('pri.der')

import threading
MINER_WORKER = None


def get_candidate_public_key_from_some_secure_channel():
    # This can be done by downloading from https servers
    return '30819f300d06092a864886f70d010101050003818d0030818902818100abfac79b3656f20de2cda012482788f78a0b6e891c6b93c946c3b14617a6aa743b49a9fbbd426245b7ef8382f20c2a6f0d29ab92699961076fe38658f4e6a4bbbdededc053aa445f78a0aaf17559ee8fea17e2f19b812201c7b4a7f8029f2df8fb030561f25d8b7e9c829530633ea1cb68aed505574c34e74b2b6e20b88d20990203010001'


def from_locoal_host(request):
    ip = None
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip == '127.0.0.1'


def return_fresh_thread(arguments):
    global blockchain
    return threading.Thread(target=blockchain.mine, args=arguments)


# Instantiate the Node
app = Flask(__name__, static_folder=sta_dir, template_folder=tmpl_dir)
CORS(app)


@app.template_filter('ctime')
def timectime(s):
    return ctime(s)  # datetime.datetime.fromtimestamp(s)


@app.route('/')
def index():
    global MINER_WORKER
    global blockchain
    table_items_outstanding = blockchain.curr_session
    # for vote_dict in blockchain.curr_session:
    #     table_items_outstanding.append(vote_dict)

    table_items_mined = blockchain.chain

    isMining = MINER_WORKER and MINER_WORKER.isAlive()
    return render_template('./index.html', index_is="isMining", table_items_outstanding=table_items_outstanding, table_items_mined=table_items_mined, isMining=isMining)


@app.route('/mine', methods=['GET'])
def start_mining():
    global blockchain
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
            (MINERS_PUBLIC_ADDRESS, MINERS_PRIVATE_ADDRESS))
        MINER_WORKER.start()
    return jsonify(response), code


@app.route('/configure')
def configure():
    global blockchain
    registered_nodes = list(blockchain.nodes)
    return render_template('./configure.html', index_is="isConfiguring", registered_nodes=registered_nodes)


@app.route('/import_id')
def new_id():
    return render_template('./import_id.html', index_is="isImporting")


@app.route('/identity/new', methods=['GET'])
def new_identity():
    response = gen_id()
    global MINERS_PRIVATE_ADDRESS
    global MINERS_PUBLIC_ADDRESS
    MINERS_PRIVATE_ADDRESS = response.pop("private_key")
    MINERS_PUBLIC_ADDRESS = response.get("public_key")
    return jsonify(response), 200

# Functions below are open to the public


@app.route('/chain', methods=['GET'])
def get_chain():
    global blockchain
    response = blockchain.export_chain()
    return jsonify(response), 200


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    # Get transactions from transactions pool
    outstanding_rslt = blockchain.curr_session

    response = {'transactions': outstanding_rslt}
    return jsonify(response), 200

@app.route('/register_nodes', methods=['POST'])
def register_nodes():
    global blockchain
    values = request.form
    required = ['nodes']
    response = {}
    if not all(k in values for k in required):
        response['error'] = "Missing values"
        return jsonify(response), 400
    if blockchain.connect_node(values['nodes']) > 0:
        response['error'] = "Invalid url"
        return jsonify(response), 400
    response['message'] = "The node is registered."
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    global blockchain
    values = request.form
    response = {}
    # Check that the required fields are in the POST'ed data
    required = ['voter_address_con', 'vote2_con', 'signature_con', 'can_sign']
    if not all(k in values for k in required):
        response['error'] = 'Missing values'
        return jsonify(response), 400
    if not verify_object_signature(get_candidate_public_key_from_some_secure_channel(), values['can_sign'], values['vote2_con']):
        response['error'] = "Invalid Candidate"
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
        app.run(host='0.0.0.0', port=port)
    except:
        dump2file(blockchain)
