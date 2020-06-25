### BloomFilters
This project aims to test BloomFilters with k-slices.  
Assume we have a giant set of English words,
user enters any string to know if the string is an English word or not.
It is important not to use a dictionary or set because of memory constraints.

#### Usage:
BloomFilters with k-slices:  
1. Clone this repo
2. Install murmur hash and bitstring:
```
         pip3 install mmh3
         pip3 install bitstring
```  
4. Run from command line (note that BloomFilter initialization may take some seconds):
```
         python3 test.py
```  
5. Enter any string to detect if it is an English word or not.

Optionally, run ```python3 no_bf.py``` (it uses Sets) to compare the memory usage with BloomFilters (both of them displays their own PIDs, find them from memory usage monitoring app in your OS). 

Scalable Bloom Filters implementation is in [sbf.py](https://github.com/AbduazizKayumov/BloomFilters/blob/master/sbf.py), run ```python3 test_sbf.py``` to see how it scales for 370K English words.

English words are from this [project](
https://github.com/dwyl/english-words/blob/master/words_alpha.txt).

License: [WTFPL](https://en.wikipedia.org/wiki/WTFPL).
