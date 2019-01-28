from collections import OrderedDict


class Vote:

  def __init__(self, sender_address, vote, miners_address, token):
    self.sender_address = sender_address
    self.vote = vote
    self.miners_address = miners_address
    self.token = token

  def __getattr__(self, attr):
    return self.data[attr]

  def to_dict(self):
    return OrderedDict({'voter_address': self.sender_address,
                        'miners_address': self.miners_address,
                        'token': self.token,  # Reward for miners
                        'voteTo': self.vote})
