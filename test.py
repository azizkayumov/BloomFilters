import unittest
from math import ceil, log2, log, floor
from filters.bf import BloomFilter
from filters.sbf import ScalableBloomFilters


class TestBloomFilters(unittest.TestCase):

    # Test for membership queries on BloomFilter
    def test_bloom_filter_membership(self):
        m = 1000  # slice size
        p = 0.001 # error probability
        bf = BloomFilter(m, p)
        max_n = bf.max_n()
        for i in range(max_n):
            bf.add(str(i))

        # check for membership
        for i in range(max_n):
            self.assertTrue(bf.contains(str(i)), "Element " + str(i) + " is not found")

    # Test for false positives on BloomFilter
    def test_bloom_filter_false_positive(self):
        m = 1000  # slice size
        p = 0.001 # error probability
        bf = BloomFilter(m, p)
        max_n = bf.max_n()

        # add elements from 0 to max_n
        for i in range(max_n):
            bf.add(str(i))

        # count false positives
        num_queries = 100000
        actual = 0
        for i in range(max_n, max_n + num_queries):
            if bf.contains(str(i)):
                actual += 1
        expected = num_queries * p
        self.assertLessEqual(actual, expected, "False positives are more than 10")

    # Test for membership queries on ScalableBloomFilters
    def test_scalable_bloom_filter_membership(self):
        m = 1000  # slice size
        p = 0.001 # error probability
        sbf = ScalableBloomFilters(m, p)
        
        num_elements = 100000
        for i in range(num_elements):
            sbf.add(str(i))

        # check for membership
        for i in range(num_elements):
            self.assertTrue(sbf.contains(str(i)), "Element " + str(i) + " is not found")

    # Test for false positives on ScalableBloomFilters
    def test_scalable_bloom_filter_false_positive(self):
        m = 1000  # slice size
        p = 0.001 # error probability
        sbf = ScalableBloomFilters(m, p)

        num_elements = 10000
        for i in range(num_elements):
            sbf.add(str(i))

        # count false positives
        num_queries = 100000
        actual = 0
        for i in range(num_elements, num_elements + num_queries):
            if sbf.contains(str(i)):
                actual += 1

        compounded_error_probability = 2 * p
        expected = num_queries * compounded_error_probability
        self.assertLessEqual(actual, expected, "False positives are more than " + str(num_queries * p))

if __name__ == "__main__":
    unittest.main(verbosity=2)
