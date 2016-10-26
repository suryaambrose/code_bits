
# Standard library
import unittest

# Local import
from decompose_number_on_base import decompose_number_on_base


def combination_iterator(*lists):
	"""
	Create a list of tuples, with every possible combinations
	of parameters from input lists

	:param lists: lists of elements to be combined
	"""
	base = [1]
	param_per_combination = len(lists)
	for range_index in range(len(lists)):
		base.append(len(lists[range_index])*base[-1])
	num_of_combinations = base.pop()

	combinations = []

	for i in range(num_of_combinations):
		elements_selected = decompose_number_on_base(i, base)
		combination = []
		for i in range(param_per_combination):
			combination.append(lists[i][elements_selected[i]])
		combinations.append(combination)

	return combinations



class TestCombination(unittest.TestCase):

	def test_combination(self):
		combinations = combination_iterator([1,2,4,8], [0,1,2,3])
		assert(len(combinations) == 16)
		assert(combinations == [
		                        [1, 0], [2, 0],
		                        [4, 0], [8, 0],
		                        [1, 1], [2, 1],
		                        [4, 1], [8, 1],
		                        [1, 2], [2, 2],
		                        [4, 2], [8, 2],
		                        [1, 3], [2, 3],
		                        [4, 3], [8, 3]
		                       ])


if __name__ == "__main__":
	unittest.main()