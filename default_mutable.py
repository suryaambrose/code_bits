"""
When a function receives an argument which, by default, receives a mutable,
a strange behavior can happen.

Indeed, the default mutable is the same at each call, therefore the "default"
can change after several calls.
"""

# Standard library
import unittest

def addElementToList(element, list_to_change=[]):
	list_to_change.append(element)
	return list_to_change

def addElementToDict(key, value, dict_to_change={}):
	dict_to_change[key] = value
	return dict_to_change

class TestListAddition(unittest.TestCase):

	def test_basic_use(self):
		assert(addElementToList(0, []) == [0])
		assert(addElementToList(1, []) == [1])

	def test_use_with_default(self):
		assert(addElementToList(0) == [0])
		res = addElementToList(1)

		## Here we might expect res to be [1]
		## But it is not because the function received
		## the same list twice. 0 was added in the first call
		## The second call added a 1, but the first 0 remains.

		with self.assertRaises(AssertionError):
			assert(res==[1])
		assert(res==[0,1])

class TestDictAddition(unittest.TestCase):

	def test_basic_use(self):
		assert(addElementToDict("a", 0, {}) == dict(a=0))
		assert(addElementToDict("b", 1, {}) == dict(b=1))

	def test_use_with_default(self):
		assert(addElementToDict("a", 0) == dict(a=0))
		res = addElementToDict("b", 1)

		## Here we might expect res to be dict(b=1)
		## But it is not because the function received
		## the same dict twice. a=0 was added in the first call
		## The second call added b=1, but the first (key,value) remains.

		with self.assertRaises(AssertionError):
			assert(res == dict(b=1))
		assert(res == dict(a=0, b=1))

if __name__ == "__main__":
	unittest.main()
