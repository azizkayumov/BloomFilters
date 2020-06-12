from math import ceil, floor, log2, log
from bitstring import BitArray
import mmh3 # murmur hash
import os # getpid
from bf import BloomFilter


class ScalableBloomFilters:
    def __init__(self, M, P, s = 2, r = 0.5):
        self.M = M
        self.P = P
        self.s = s
        self.r = r
        self.p = 0.5 # fill ratio
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


    def create_filter(self):
        i = len(self.filters)

        Pi = self.P * self.r
        self.P = self.P - Pi

        Mi = self.M * (self.s ** i)
        Ni = self.max_n(Mi, Pi)

        new_filter = BloomFilter(Ni, Pi)
        self.filters.append(new_filter)


    def max_n(self, M, P):
        return floor(-1 * M * log(self.p) * log(1 - self.p) / log(P))
