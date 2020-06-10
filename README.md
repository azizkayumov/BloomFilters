### BloomFilters
This project aims to test BloomFilters with k-slices.  
Assume we have a giant set of English words,
user enters any string to know if the string is an English word or not.
It is important not to use a dictionary or set because of memory constraints.

Steps to follow before using:
1. Download [bf.py](https://github.com/AbduazizKayumov/BloomFilters/blob/master/bf.py)
2. Download English words from to this [project](
https://github.com/dwyl/english-words/blob/master/words_alpha.txt).
3. Install murmur hash and bitstring:
```
         pip3 install mmh3
         pip3 install bitstring
```  
4. Run bf.py from command line:
         python3 bf.py    
Note that BloomFilter initialization may take some seconds.
5. Enter any string to detect if it is an English word or not.

License: [WTFPL](https://en.wikipedia.org/wiki/WTFPL).
