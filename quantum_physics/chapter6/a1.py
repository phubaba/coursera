import random, math, pylab
from scipy.stats import truncnorm

def gauss_cut():
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= 1.0:
            return x

uniform = False

alpha = 0.5
nsamples = 100000
samples_x = []
samples_y = []
normalization = truncnorm.pdf(0, -1.0, 1.0) ** 2.
for sample in xrange(nsamples):
    while True:
	if uniform:
		x = random.uniform(-1.0, 1.0)
		y = random.uniform(-1.0, 1.0)
	else:
		x = gauss_cut()
		y = gauss_cut()

        p = math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4))
	if not uniform:
		p = p/(truncnorm.pdf(x, -1.0, 1.0) * truncnorm.pdf(y, -1.0, 1.0) / normalization)
        if random.uniform(0.0, 1.0) < p:
            break
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A1_1')
if uniform:
	pylab.savefig('plot_A1_1_uniform.png')
else:
	pylab.savefig('plot_A1_1.png')
pylab.show()
