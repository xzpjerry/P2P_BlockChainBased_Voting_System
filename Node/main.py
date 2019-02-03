import sys
sys.path.append("./Modal")
sys.path.append("./View")
sys.path.append("./Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from blockChain import Blockchain
from vote import Vote
from core_logic import submit_transaction, mine, gen_id


import requests
from flask import Flask, jsonify, request, render_template

# Allowing request from other server(node)
from flask_cors import CORS

# Handling path string
import os
tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'View/templates')
sta_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'View/static')

# Instantiate the Blockchain
blockchain = Blockchain()

import threading
def return_fresh_thread():
    return threading.Thread(target=mine, args=(blockchain,))
MINER_WORKER = False

# Instantiate the Node
app = Flask(__name__, static_folder=sta_dir, template_folder=tmpl_dir)
CORS(app)

MINERS_PUBLIC_ADDRESS = None

@app.route('/')
def index():
    global MINER_WORKER
    table_items_outstanding = []
    for vote_dict in blockchain.curr_session:
        table_items_outstanding.append(vote_dict)

    table_items_mined = []
    for block in blockchain.chain:
        for vote_dict in block['history']:
            table_items_mined.append(vote_dict)

    isMining = MINER_WORKER and MINER_WORKER.isAlive()
    return render_template('./index.html', table_items_outstanding = table_items_outstanding, table_items_mined = table_items_mined, isMining = isMining)


@app.route('/configure')
def configure():
    return render_template('./configure.html')

@app.route('/new_id')
def new_id():
    return render_template('./new_id.html')

@app.route('/identity/new', methods=['GET'])
def new_identity():
    response = gen_id()

    # priK = response['private_key']
    # pubK = response['public_key']

    # for candidate in CANDIDATES.as_list():
    #     print(sign_transaction(candidate, priK))

    return jsonify(response), 200

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    #Get transactions from transactions pool
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
    rslt = submit_transaction(blockchain, values['voter_address_con'], values['vote2_con'], values['signature_con'])

    if rslt == -1:
        response['error'] = 'Invalid Vote!'
        return jsonify(response), 400
    response = {'message': 'Transaction will be added to Block soon.'}
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def start_mining():
    global MINER_WORKER
    if MINER_WORKER and MINER_WORKER.isAlive():
        return "Nonsense!", 400
    MINER_WORKER = return_fresh_thread()
    MINER_WORKER.start()
    return "Will do", 200

@app.route('/nodes/log_in', methods=['POST'])
def register_nodes():
    values = request.form
    address = values.get('miners_address')

    if not address:
        return "Error: Please supply a valid address", 400

    MINERS_PUBLIC_ADDRESS = address
    print(MINERS_PUBLIC_ADDRESS)
    response = {
        'message': 'Your address is set',
    }
    return jsonify(response), 201

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)

# if __name__ == "__main__":
#     test = Blockchain()
#     print(test)
#     # print(submit_transaction(test, "NotValiate", "Alice", 0))
#     test_kpub = "30819f300d06092a864886f70d010101050003818d0030818902818100e3e1d0eaff59308ba06800c1298b0ebb15af0f98ddd349fce6afca84644099cfa170e848ba4cacb232d61301ebcc454b6c03bc6d61dd66fe7d66acd8e6655366d76e0e554cad7dcce53ecfef2a8ad1ac542dab8a44e9efa0e1e64c405f8ee0dd90ef84f5fd11b3ec30a0bc7652336065d248242d3de40a40191932f8b39d62e50203010001"
#     test_sign = "e1b4ef9444a3046b107132edf461c1bdd6bad5eac688803e3d0eb8b29d2e23c6ac6c8a64eac0a035fcd241d6af643d003a31c2a76bdf89c6411b4ccca88aa72e36c09c7504c08fe66c7c5c93b818b2143e61caa0584f6d5711fb2a87d2629e369f6716e6c3aabb72275d99c8ccd6061b0a8dcf3676985e506a032d064e0d1161"
#     submit_transaction(test, test_kpub, "Alice", test_sign)

#     mine(test)
#     print(test)

#     # Eve wants to tamper the vote to Bob
#     # will not work, the submission would return -1
#     # print(submit_transaction(test, test_kpub, "Bob", test_sign))

#     mine(test)
#     print(test)
