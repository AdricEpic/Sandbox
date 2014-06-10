import timeit

setup_10x10 = """
import ascii_screen as scr

testScreen = scr.Screen(10, 10)
"""
results10 = timeit.Timer(stmt="testScreen.show()", setup=setup_10x10).repeat(10, 12)
avgResults10 = sum(results10) / float(len(results10))

setup_100x100 = """
import ascii_screen as scr

testScreen = scr.Screen(100, 100)
"""
results100 = timeit.Timer(stmt="testScreen.show()", setup=setup_100x100).repeat(10, 12)
avgResults100 = sum(results100) / float(len(results100))


print " 10 x  10 - Min: %f, Max: %f, Avg: %f" % (min(results10), max(results10), avgResults10)
print "100 x 100 - Min: %f, Max: %f, Avg: %f" % (min(results100), max(results100), avgResults100)