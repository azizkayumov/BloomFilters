import unittest
import random

from filters.bf import BloomFilter
from filters.sbf import ScalableBloomFilters


class TestBloomFilters(unittest.TestCase):

    # Test for membership queries on BloomFilter
    def test_membership(self):
        N = 100000
        P = 0.001
        bf = BloomFilter(N, P)
        for i in range(N):
            element = str(i)
            bf.add(element)

        for i in range(N):
            test_element = str(i)
            may_contain = bf.contains(test_element)
            self.assertEqual(may_contain, True, "A membership query on " + str(test_element) + " must be True, the result was False")


    # Test if the false positive error probability is less than the desired value
    def test_false_positive(self):
        N = 100000
        P = 0.001
        bf = BloomFilter(N, P)

        # insert random numbers
        not_inserted = []
        for i in range(N):
            element = str(i)
            insert = random.choice([True, False])
            if insert:
                bf.add(element)
            else:
                not_inserted.append(i)

        # check for not inserted numbers
        # count the false positive queries
        number_of_false_positives = 0
        for element in not_inserted:
            test_element = str(element)
            may_contain = bf.contains(test_element)
            if may_contain:
                number_of_false_positives += 1

        false_positive_error = number_of_false_positives / N
        self.assertLessEqual(false_positive_error, P, "False positive error must be less than the desired value")


    # Test that new additions are not possible if already filled up
    def test_addition_impossible(self):
        N = 100000
        P = 0.001
        bf = BloomFilter(N, P)
        for i in range(N):
            element = str(i)
            bf.add(element)

        new_element = N + 1
        added = bf.add(new_element)

        self.assertEqual(added, False, "New additions should have been impossible")


    # Test if ScalableBloomFilters maximizes N for its first filter
    # such that its filters allocate space less than or equal to the desired M
    def test_sbf_scalability(self):
        M = 64
        P = 0.001

        sbf = ScalableBloomFilters(M, P)

        number_of_filters = 20
        desired_M = M
        allocated_M = sbf.filters[-1].m * sbf.filters[-1].k

        for i in range(1, number_of_filters):
            desired_M += M * (sbf.s ** i)

            sbf.create_filter()
            filter = sbf.filters[-1]
            allocated_M = filter.m * filter.k

        self.assertLessEqual(allocated_M, desired_M, "ScalableBloomFilters allocated more space than expected")


    # Test that ScalableBloomFilter's compounded error probability stays under the desired value
    def test_sbf_compounded_error_probability(self):
        M = 64
        P = 0.001

        sbf = ScalableBloomFilters(M, P)

        number_of_filters = 20
        compounded_error_prob = sbf.filters[-1].P
        for i in range(number_of_filters):
            sbf.create_filter()
            compounded_error_prob += sbf.filters[-1].P

        self.assertLessEqual(compounded_error_prob, P, "ScalableBloomFilters error probability exceeds the desired value")


if __name__ == "__main__":
    unittest.main(verbosity=2)
