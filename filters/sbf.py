from math import ceil, floor, log2, log
from filters.bf import BloomFilter


class ScalableBloomFilters:
    def __init__(self, m, p, s = 2, r = 0.5):
        self.m = m      # available bits for the first filter (slice size)
        self.p = p      # overall error probability
        self.s = s      # slice scale factor
        self.r = r      # tightening ratio
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
        pi = self.p * self.r
        # subtract the new error probability from overall error probability
        self.p -= pi

        # scale the slice size for new filter: Mi = M * s ^ i
        mi = self.m * (self.s ** i)

        new_filter = BloomFilter(mi, pi)
        self.filters.append(new_filter)
