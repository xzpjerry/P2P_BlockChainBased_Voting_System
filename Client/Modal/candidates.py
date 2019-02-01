"""
A list of candidates'name
"""


class Candidates():
    """
    A list of candidates'name
    Can be instantiated with a file
    """

    def __init__(self, theList="res/candidates.txt"):
        self.candidates = []
        self.candidates_signature_pair_list = []
        if isinstance(theList, str):
            with open(theList, 'r') as f:
                for line in f.readlines():
                    if len(line) == 0 or line.startswith("#"):
                        continue
                    name_sign_list = line.strip().split(' ')
                    if len(name_sign_list) != 2:
                        continue
                    self.candidates.append(name_sign_list[0])
                    self.candidates_signature_pair_list.append(
                        (name_sign_list[0], name_sign_list[1]))
        self.candidates.sort()

    def as_list(self):
        return self.candidates

    def as_list_with_signature(self):
        return self.candidates_signature_pair_list
