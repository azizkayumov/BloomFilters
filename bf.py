from math import ceil, log2, log, floor
from bitstring import BitArray
import mmh3 # murmur hash


class BloomFilter:
    def __init__(self, N, P):
        p = 1 / 2 # fill ratio

        self.P = P
        self.N = N
        self.m = ceil(- N / log(p))
        self.k = floor(log2(1 / P))
        self.slices = []
        for i in range(self.k):
            self.slices.append(BitArray(self.m))

        self.count = 0

    def add(self, value):
        if self.count >= self.N:
            return False

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
