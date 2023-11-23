from math import ceil, log2, log, floor
from bitstring import BitArray
import mmh3 # murmur hash


class BloomFilter:
    def __init__(self, m, p):
        self.m = m                      # slice size
        self.p = p                      # error probability
        self.k = floor(log2(1 / p))      # number of slices
        self.n = self.max_n()           # number of elements
        self.count = 0                  # number of elements inserted

        # add k slices
        self.slices = []
        for _ in range(self.k):
            self.slices.append(BitArray(self.m))

    def add(self, value):
        # if this BloomFilter was already filled up
        # return False indicating that "I cannot house more elements"
        if self.count >= self.n:
            return False

        # set bits
        for slice in range(self.k):
            index = self.hash(slice, value)
            self.slices[slice][index] = 1

        self.count += 1
        return True

    def contains(self, value):
        for slice in range(self.k):
            index = self.hash(slice, value)
            if self.slices[slice][index] == 0:
                return False
        return True

    def hash(self, seed, value):
        h = mmh3.hash(value, seed)
        return h % self.m
    
    # maximizes N for given error probability P and filter size M
    def max_n(self):
        M = self.m * self.k
        P = self.p
        max_n = (M * (log(2) ** 2)) / abs(log(P))
        return floor(max_n)
    
    def __to_str__(self):
        return "BloomFilter(m = " + str(self.m) + ", p = " + str(self.p) + ", k = " + str(self.k) + ", n = " + str(self.n) + ")"
