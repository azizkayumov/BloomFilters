import os


file = open("words.txt",'r')
words = file.read().splitlines()

S = set(words)

print("PID = ", os.getpid())

s = input("Enter any word: ")
while s:
    if s in S:
        print(s + " is an English word.\n")
    else:
        print(s + " is not an English word.\n")
    s = input("Enter any word: ")
