from math import ceil, floor, log2, log
from filters.bf import BloomFilter


class ScalableBloomFilters:
    def __init__(self, M, P, s = 2, r = 0.5):
        self.M = M      # available bits for the first filter
        self.P = P      # overall error probability
        self.s = s      # slice scale factor
        self.r = r      # tightening ratio
        self.p = 0.5    # fill ratio
        self.filters = []

        # create first BloomFilter
        self.create_filter()

    def add(self, value):
        # try to add to the last filter
        added = self.filters[-1].add(value)

        # if couldn't add to the last filter,
        # create new filter with tighter error probability
        if not added:
            self.create_filter()
            self.add(value)


    def contains(self, value):
        # membership queries are done on each filter
        # if any filter may contain the value, return True
        for filter in self.filters:
            may_contain = filter.contains(value)
            if may_contain:
                return True

        return False


    def create_filter(self):
        i = len(self.filters)

        # get new error probability with the tightening ratio
        Pi = self.P * self.r
        # subtract the new error probability from overall error probability
        self.P = self.P - Pi

        # scale the slice size for new filter: Mi = M * s ^ i
        Mi = self.M * (self.s ** i)
        # maximize N for new filter
        Ni = self.max_n(Mi, Pi)

        new_filter = BloomFilter(Ni, Pi)
        self.filters.append(new_filter)


    # maximizes N for given error probability P and filter size M
    def max_n(self, M, P):
        return floor(-1 * M * log(self.p) * log(1 - self.p) / log(P))
