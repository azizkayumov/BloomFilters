from math import ceil, log2, log
from bitstring import BitArray
import mmh3 # murmur hash
import os # get pid


class BloomFilter:
    def __init__(self, N, P):
        p = 1 / 2
        self.m = ceil(- N / log(p))
        self.k = ceil(log2(1 / P))
        self.slices = []
        for i in range(self.k):
            self.slices.append(BitArray(self.m))

    def add(self, value):
        for slice in range(self.k):
            index = self.hash(slice, value)
            self.slices[slice][index] = 1

    def contains(self, value):
        for slice in range(self.k):
            index = self.hash(slice, value)
            if self.slices[slice][index] == 0:
                return False
        return True

    def hash(self, seed, value):
        value = value.lower()
        h = mmh3.hash(value, seed)
        return h % self.m


file = open("words.txt",'r')
words = file.read().splitlines() # to ignore '\n's

N = len(words)
P = 0.001
bf = BloomFilter(N, P)
print("BloomFilter initialized with: ")
print("m = ", bf.m)
print("k = ", bf.k)
print("N = ", N)

for word in words:
    bf.add(word)

print("PID = ", os.getpid())

s = input("Enter any word: ")
while s:
    if bf.contains(s):
        print(s + " may be an English word.\n")
    else:
        print(s + " is not an English word.\n")
    s = input("Enter any word: ")
