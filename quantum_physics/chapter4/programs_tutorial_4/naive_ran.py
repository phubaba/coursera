import numpy
m = 134456
n = 8121
k = 28411
idum = 1000
vals = []

for iteration in xrange(200000):
    idum = (idum *  n + k) % m
    ran = idum / float(m)
    # print idum, ran, iteration
    vals.append(idum)

vals = numpy.unique(numpy.array(vals))
print min(vals), max(vals)
print min(vals[1:] - vals[0:-1]), max(vals[1:] - vals[0:-1])
