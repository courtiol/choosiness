import random
from collections import Counter

# alias method
class Alias(object):
    def __init__(self, keys):
        # make either a copy of 'keys' or turn it into a list if it's a
        # generator. needed because of double traversal below
        keys = list(keys)
        # distribute items into two lists and calc their average
        avg = float(sum(ki[1] for ki in keys)) / len(keys)
        gt = []
        lt = []
        for ki in keys:
            if ki[1] < avg:
                lt.append(ki)
            else:
                gt.append(ki)

        # build the alias structure
        self.alias = []
        while lt:
            li = lt.pop(0)
            gi = gt.pop(0)
            self.alias.append((li[1] / avg, li[0], gi[0]))
            gi = (gi[0], gi[1] + li[1] - avg)
            if gi[1] >= avg or not gt:
                # put back into gt if gi is still greater than average or if gt
                # would become empty, which can happen due to rounding errors
                gt.append(gi)
            else:
                lt.append(gi)
        for gi in gt:
            self.alias.append((1.0, gi[0], None))
        self.aliaslen = len(self.alias)

    def get(self):
        """Return a random element."""
        n = self.aliaslen * random.random()
        nint = int(n)
        ai = self.alias[nint]
        return ai[1 if (n - nint) < ai[0] else 2]

# stochiastic acceptance method
class Roulette(object):
    def __init__(self, keys):
        keys = list(keys)
        pmax = float(max(p for _, p in keys))
        psum = float(sum(p for _, p in keys))
        pmax /= psum
        self._len = len(keys)
        self.keys = [(val, p / psum / pmax) for val, p in keys]

    def get(self):
        """Return a random element."""
        while 1:
            p = random.random() * self._len
            pint = int(p)
            if self.keys[pint][1] >= p - pint:
                return self.keys[pint][0]


vals = [('a', 4), ('b', 3), ('c', 2), ('d', 1)]

a = Alias(vals)
r = Roulette(vals)

def test(n):
    return Counter(a.get() for _ in range(n)) # xrange changed to range for python3 compatibility
