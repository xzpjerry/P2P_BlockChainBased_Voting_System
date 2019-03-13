from collections import OrderedDict


class Vote:

    def __init__(self, sender_address, vote):
        self.sender_address = sender_address
        self.vote = vote

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        rslt = OrderedDict()
        rslt['voter_address'] = self.sender_address,
        rslt['miners_address'] = None,
        rslt['token'] = None,
        rslt['voteTo'] = self.vote
        return rslt
