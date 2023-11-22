import unittest
import random

from filters.bf import BloomFilter
from filters.sbf import ScalableBloomFilters


class TestBloomFilters(unittest.TestCase):

    # Test for membership queries on BloomFilter
    def test_membership(self):
        m = 64
        p = 0.001
        sbf = ScalableBloomFilters(m, p)
        
        num_elements = 10000
        for i in range(num_elements):
            element = str(i)
            sbf.add(element)

        for i in range(num_elements):
            test_element = str(i)
            may_contain = sbf.contains(test_element)
            self.assertEqual(may_contain, True, "A membership query on " + str(test_element) + " must be True, the result was False")

    # Test for membership queries on BloomFilter
    def test_false_positive(self):
        m = 64
        p = 0.001
        sbf = ScalableBloomFilters(m, p)
        num_elements = 10000
        for i in range(num_elements):
            element = str(i)
            sbf.add(element)

        num_false_positives = 0
        num_queries = 0
        for i in range(num_elements, num_elements * 20):
            test_element = str(i)
            if sbf.contains(test_element):
                num_false_positives += 1
            num_queries += 1
            
        self.assertLessEqual(num_false_positives / num_queries, p, "False positive rate is greater than expected")


    # Test if ScalableBloomFilters maximizes N for its filters
    # such that its filters allocate space less than or equal to the desired M
    def test_sbf_scalability(self):
        m0 = 64
        p = 0.001
        slice_growth = 2
        sbf = ScalableBloomFilters(m0, p, s = slice_growth)
        k0 = sbf.filters[-1].k

        number_of_filters = 20
        for i in range(1, number_of_filters):
            filter = sbf.filters[-1]
            expected = m0 * (slice_growth ** i) * (k0 + i) # adds one more hash function for each filter

            sbf.create_filter()
            filter = sbf.filters[-1]
            actual = filter.m * filter.k
            self.assertLessEqual(actual, expected, "ScalableBloomFilters allocated more space than expected")
        

    # Test that ScalableBloomFilter's compounded error probability stays under the desired value
    def test_sbf_compounded_error_probability(self):
        m = 64
        p = 0.001
        sbf = ScalableBloomFilters(m, p)

        compounded_error_prob = sbf.filters[-1].p
        number_of_filters = 20
        for i in range(number_of_filters):
            sbf.create_filter()
            compounded_error_prob += sbf.filters[-1].p
        self.assertLessEqual(compounded_error_prob, p, "ScalableBloomFilters error probability exceeds the desired value")



if __name__ == "__main__":
    unittest.main(verbosity=2)
