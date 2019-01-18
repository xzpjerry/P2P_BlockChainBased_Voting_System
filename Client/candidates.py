"""
A list of candidates'name
"""


class Candidates():
    """
    A list of candidates'name
    Can be instantiated with a file
    """

    def __init__(self, theList="Client/res/candidates.txt"):
        self.candidates = []
        if isinstance(theList, str):
            with open(theList, 'r') as f:
                for line in f.readlines():
                    if len(line) == 0 or line.startswith("#"):
                        continue
                    self.candidates.append(line.strip())
        self.candidates.sort()

    def as_list(self):
        return self.candidates
