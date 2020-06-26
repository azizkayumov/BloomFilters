import os # get pid
from sbf import ScalableBloomFilters


sbf = ScalableBloomFilters(64, 0.001)

file = open("words.txt",'r')
words = file.read().splitlines() # to ignore '\n's
for word in words:
    sbf.add(word)

compounded_error_prob = 0
for i in range(len(sbf.filters)):
    bf = sbf.filters[i]
    print("----------- BloomFilter[" + str(i) + "]-----------")
    print("N = ", bf.N)
    print("k = ", bf.k)
    print("P = ", bf.P)
    print("m = ", bf.m)
    compounded_error_prob += bf.P

print("Overall P = ", compounded_error_prob)

print("PID = ", os.getpid())

s = input("Enter any word: ")
while s:
    if sbf.contains(s):
        print(s + " may be an English word.\n")
    else:
        print(s + " is not an English word.\n")
    s = input("Enter any word: ")
