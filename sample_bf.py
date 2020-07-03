import os # get pid
from filters.bf import BloomFilter


file = open("data/words.txt",'r')
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
