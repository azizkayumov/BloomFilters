import os # get pid
from filters.sbf import ScalableBloomFilters


sbf = ScalableBloomFilters(64, 0.001)

file = open("data/words.txt",'r')
words = file.read().splitlines() # to ignore '\n's
for word in words:
    sbf.add(word)

compounded_error_prob = 0
compounded_memory_usage = 0
for i in range(len(sbf.filters)):
    bf = sbf.filters[i]
    print("----------- BloomFilter[" + str(i) + "]-----------")
    print("N = ", bf.max_n())
    print("k = ", bf.k)
    print("P = ", bf.p)
    print("m = ", bf.m)
    compounded_error_prob += bf.p
    compounded_memory_usage += bf.m * bf.k

print("Overall P = ", compounded_error_prob)
print("Overall M = ", compounded_memory_usage, " bits")

print("PID = ", os.getpid(), "\n")

s = input("Enter any word: ")
while s:
    if sbf.contains(s):
        print(s + " may be an English word.\n")
    else:
        print(s + " is not an English word.\n")
    s = input("Enter any word: ")
