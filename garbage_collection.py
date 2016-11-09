# Explanations from http://www.digi.com/wiki/developer/index.php/Python_Garbage_Collection
# A part of the code also comes from there

"""
Deallocation of memory is done in Python via two things:
- ref counting
- garbage collection

Ref counting counts each reference to an object from the moment it is allocated. Once this number
reaches 0, the object is deallocated.
But sometimes, ref counting does not work, for instance when an object has a reference to itself,
of when two objects have reference to eah other, although they are not used anymore.
This is where garbage collection comes into the game, to find and destroy those objects
"""

import gc

def make_unreachable_object():
	l = []

def make_unreachable_object_with_ref_cycles():
	l=[]
	l.append(l)
	return l

def make_uncollectable_object():
	class Child:
		def __init__(self, parent):
			self.parent = parent

		def __del__(self):
			self.parent = None

	class Parent:
		def makeChild(self):
			self.child = Child(self)

		def __del__(self):
			self.child = None

	p=Parent()
	p.makeChild()

def main():
	print "\tCreating 1 unreachable object => should be destroyed automatically"
	make_unreachable_object()

	print "\tCollect...=> no unreachable or uncollectable should be visible"
	collected = gc.collect(0)
	assert(collected == 0)
	assert(gc.garbage == [])

	print "\tCreating 1 unreachable object with ref cycles"
	make_unreachable_object_with_ref_cycles()
	print "\tCollect...=> 1 unreachable and 0 uncollectable should be visible"
	collected = gc.collect(0)
	assert(collected == 1)
	assert(gc.garbage == [])

	print "\tCreating 1 uncollectable object"
	make_uncollectable_object()
	print "\tCollect...=> Unreachables and uncollectables should be visible"
	collected = gc.collect(0)
	assert(collected != 0)
	assert(gc.garbage != [])

if __name__ == "__main__":
	gc.disable() # disable automatic garbage collection
	gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS) # activate gc debug flags
	main()
	gc.set_debug(0) # deactivate gc debug flags