from collections import OrderedDict
class Vote:

    def __init__(self, sender_address, vote):
        self.sender_address = sender_address
        self.vote = vote

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'voter_address': self.sender_address,
                           'miners_address': None,
                           'token': None,  # Reward for miners
                           'voteTo': self.vote})