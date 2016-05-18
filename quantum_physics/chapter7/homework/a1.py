import math, pylab

import math, random, pylab
import numpy

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
high = low[:]
data = []
for step in xrange(nsteps):
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    data+=low[:]

# graphics output
pylab.hist(data, normed=True, bins=100, label='Low')

list_x = numpy.linspace(-5, 5, 100)
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='analytic')

pylab.xlabel('x', fontsize=16)
pylab.ylabel('$\pi$(x)', fontsize=16)
pylab.title('Distinguishable particle histogram', fontsize=16)
pylab.legend(loc='upper left')
pylab.savefig('a1.png')
pylab.show()
