import math
import numpy

degrees_offset = 15

radians = lambda degrees: degrees/360. * 2 * math.pi
toDegrees = lambda radians: radians * 360 / (2 * math.pi)

def calc_psi_6(degrees_offset, numberOfNeighbors=6):
    all_offsets = numpy.array([radians(degrees_offset + i*60) for i in xrange(numberOfNeighbors)])
    psi_6 = 1/float(numberOfNeighbors) * numpy.sum(numpy.exp(6 * 1j * all_offsets))
    return psi_6, all_offsets

psi_6, all_offsets = calc_psi_6(degrees_offset)

print "circle offsets: %s" % map(toDegrees, all_offsets)
print "psi_6: %s" % psi_6

psi_6ab = calc_psi_6(0)[0] + calc_psi_6(30)[0]

print "psi_6(0 degrees) + psi_6(30 degrees): %s" % psi_6ab
