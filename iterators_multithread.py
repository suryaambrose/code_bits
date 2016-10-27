import threading
import time

## From http://anandology.com/blog/using-iterators-and-generators/

# Utilities to repeat functions

def loop(func, n):
    """Runs the given function n times in a loop.
    """
    for i in range(n):
        func()

def run(f, repeats=1000, nthreads=10):
    """Starts multiple threads to execute the given function multiple
    times in each thread.
    """
    # create threads
    threads = [threading.Thread(target=loop, args=(f, repeats))
               for i in range(nthreads)]

    # start threads
    for t in threads:
        t.start()

    # wait for threads to finish
    for t in threads:
        t.join()


## Unsafe

def unsafeGenerator():
    i = 0
    while True:
        i += 1
        yield i

class UnsafeIterator:
    def __init__(self):
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
        self.i += 1
        return self.i

def unsafe():
    c1 = unsafeGenerator()
    c2 = UnsafeIterator()

    repeats = 100000
    threads = 3

    print "Call unsafe generator => raises"
    run(c1.next, repeats=repeats, nthreads=threads)
    print "UnsafeGenerator, %d == %d"%(c1.next(), repeats*threads+1)

    time.sleep(0.5)

    print "Call unsafe iterator => no exceptions, but wrong result"
    # call c2.next 100K times in 2 different threads
    run(c2.next, repeats=repeats, nthreads=threads)
    print "UnsafeIterator, %d == %d"%(c2.next(), repeats*threads+1)

    time.sleep(0.5)


## Safe

# Making a safe iterator from an unsafe one is easy

class SafeIterator:
    def __init__(self):
        self.i = 0
        # create a lock
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        # acquire/release the lock when updating self.i => sufficient
        with self.lock:
            self.i += 1
        return self.i

# Making a safe generator is a bit more complicated, as you cannot change
# its `next` method to protect it, so it needs to be wrapped

# You can use this kind of class
class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            return self.it.next()

# And you can also make a decorator with it
def threadsafe(f):
    """A decorator that takes a generator function and makes it thread-safe.
    """
    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))
    return g

@threadsafe
def safeGenerator():
    i = 0
    while True:
        i += 1
        yield i

def safe():
    c3 = safeGenerator()
    c4 = threadsafe_iter(unsafeGenerator())
    c5 = SafeIterator()

    repeats = 100000
    threads = 3

    print "Call safe generator => OK"
    run(c3.next, repeats=repeats, nthreads=threads)
    print "SafeGenerator, %d == %d"%(c3.next(), repeats*threads+1)

    time.sleep(0.5)

    print "Call unsafe generator made safe => OK"
    run(c4.next, repeats=repeats, nthreads=threads)
    print "SafeGenerator, %d == %d"%(c4.next(), repeats*threads+1)

    time.sleep(0.5)

    print "Call safe iterator => OK"
    run(c5.next, repeats=repeats, nthreads=threads)
    print "SafeIterator, %d == %d"%(c5.next(), repeats*threads+1)

    time.sleep(0.5)

def main():
    unsafe()
    safe()

if __name__ == "__main__":
    main()