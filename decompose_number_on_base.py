
# Standard library
import unittest

def decompose_number_on_base(number, base):
	"""
	Returns a number's decomposition on a defined base

	:param number: The number to decompose
	:param base: list representing the base. It must be sorted and
	each element must be a multiple of its predecessor. First element
	must be 1.
	:raises TypeError: if base is invalid
	"""
	_base = list(base)
	try:
		assert(_base[0] == 1)
		for i in range(1, len(_base)):
			assert(_base[i] > _base[i-1])
			ratio = float(_base[i]) / float(_base[i-1])
			assert(ratio == int(ratio))
	except AssertionError:
		raise TypeError("Base (%s) is invalid"%_base)

	_base.reverse()
	output = [0]*len(_base)
	for base_index in range(len(_base)):
		r = number % _base[base_index]
		output[base_index] = int((number-r)/_base[base_index])
		number = r

	output.reverse()
	return output


class TestDecomposition(unittest.TestCase):

	def test_decomposition(self):

		with self.assertRaises(TypeError):
			# Does not start with 1
			decompose_number_on_base(10, [2,3])

		with self.assertRaises(TypeError):
			# Not sorted
			decompose_number_on_base(10, [1,4,2])

		with self.assertRaises(TypeError):
			# Not all elements are multiple of the previous element
			decompose_number_on_base(10, [1,2,3])

		assert(decompose_number_on_base(10, [1,2,4,8]) == [0,1,0,1]) # binary base
		assert(decompose_number_on_base(10, [1,10,100]) == [0,1,0]) # decimal base
		assert(decompose_number_on_base(10, [1,16,256]) == [10,0,0]) # hexadecimal base
		assert(decompose_number_on_base(10, [1,8,64]) == [2,1,0]) # octal base
		assert(decompose_number_on_base(100, [1,2,6,18,36]) == [0,2,1,1,2])


if __name__ == "__main__":
	unittest.main()