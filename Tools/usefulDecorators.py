__author__ = 'robert'

import time

def printAllParameters(__str__):
    """
    Decorator for __str__. After applying the method prints the values of all parameters of the class
    :param __str__:
    :return:new __str__ method
    """
    def new_str(*args):
        z = ""
        for key in args[0].__dict__.keys():
            z += key+": "+str(args[0].__dict__[key])+"\n"
        z += __str__(*args)
        return z
    return new_str

def measure_time(timed_method):
    """
    Decorator for measuring the executing time
    source: https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
    :param timed_method:
    :return:
    """
    def timed(*args, **kw):
        ts = time.time()
        result = timed_method(*args, **kw)
        te = time.time()

        #print('%r (%r, %r) %2.2f sec' % \
        #      (timed_method.__name__, args, kw, te-ts))
        print(te-ts)
        return result

    return timed


def measure_percentage_of_time(timed_method):
    """
    Measures of every decorated function the total running time (over several iterations) and calculates
    the proportion in running time relative to all measured functions.

    (This should probably not be done like this - but works.)
    :param timed_method:
    :return:
    """
    def print_results():
        print(measure_percentage_of_time.measured_times)
        print("total_time: "+str(measure_percentage_of_time.total_time))
        print("In percentage: ")
        for measurement in measure_percentage_of_time.measured_times:
            measure_percentage_of_time.measured_times[measurement] /= measure_percentage_of_time.total_time
            measure_percentage_of_time.measured_times[measurement] *= 100
        print(measure_percentage_of_time.measured_times)

    def timed(*args, **kw):
        #measure time to run the method
        ts = time.time()
        result = timed_method(*args, **kw)
        te = time.time()

        #check if function got measured before
        runtime = measure_percentage_of_time.measured_times.get(timed_method.__name__)
        if runtime is not None:
            runtime += te-ts
        else:
            runtime = te-ts
        measure_percentage_of_time.measured_times[timed_method.__name__] = runtime
        measure_percentage_of_time.total_time += te-ts
        return result
    measure_percentage_of_time.measured_times = {}
    measure_percentage_of_time.total_time = 0
    measure_percentage_of_time.print_results = print_results
    return timed

class Tester:
    @measure_percentage_of_time
    #@measure_time
    def testA(self,nix):
        print(nix)
    @measure_percentage_of_time
    def testB(self,nix):
        print(nix)

"""
Example of using @measure_percentage_of_time:


class Tester:
    @measure_percentage_of_time
    #@measure_time
    def testA(self,nix):
        print(nix)
    @measure_percentage_of_time
    def testB(self,nix):
        print(nix)

tester = Tester()
for a in range(100):
    tester.testA("A")
for b in range(100):
    tester.testB("B")
measure_percentage_of_time.print_results()
"""
