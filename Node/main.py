import sys
sys.path.append("./Modal")
sys.path.append("./View")
sys.path.append("./Controller")
sys.path.append("Node/Modal")
sys.path.append("Node/View")
sys.path.append("Node/Controller")

from blockChain import Blockchain
from vote import Vote
from core_logic import submit_transaction, mine

if __name__ == "__main__":
    test = Blockchain()
    print(test)
    # print(submit_transaction(test, "NotValiate", "Alice", 0))
    test_kpub = "30819f300d06092a864886f70d010101050003818d0030818902818100e3e1d0eaff59308ba06800c1298b0ebb15af0f98ddd349fce6afca84644099cfa170e848ba4cacb232d61301ebcc454b6c03bc6d61dd66fe7d66acd8e6655366d76e0e554cad7dcce53ecfef2a8ad1ac542dab8a44e9efa0e1e64c405f8ee0dd90ef84f5fd11b3ec30a0bc7652336065d248242d3de40a40191932f8b39d62e50203010001"
    test_sign = "e1b4ef9444a3046b107132edf461c1bdd6bad5eac688803e3d0eb8b29d2e23c6ac6c8a64eac0a035fcd241d6af643d003a31c2a76bdf89c6411b4ccca88aa72e36c09c7504c08fe66c7c5c93b818b2143e61caa0584f6d5711fb2a87d2629e369f6716e6c3aabb72275d99c8ccd6061b0a8dcf3676985e506a032d064e0d1161"
    submit_transaction(test, test_kpub, "Alice", test_sign)

    mine(test)
    print(test)

    # Eve wants to tamper the vote to Bob
    # will not work, the submission would return -1
    # print(submit_transaction(test, test_kpub, "Bob", test_sign))

    mine(test)
    print(test)