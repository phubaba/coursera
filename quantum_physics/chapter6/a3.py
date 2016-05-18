import random, math, pylab
from scipy import integrate
from scipy.stats import truncnorm

alpha = -1.
nsteps = 1000000
samples_x = []
samples_y = []
x, y = 0.0, 0.0

uniform = False

def one_dim_f(x, alpha):
    return math.exp(-0.5 * x ** 2 - alpha * x ** 4 )

def gauss_cut():
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= 1.0:
            return x

area = integrate.quad(one_dim_f, -1, 1, args=(alpha, ))[0]
print area

import random, math, pylab
minVal = truncnorm.pdf(-1, -1., 1.)

alpha = 0.5
nsteps = 100000
samples_x = []
samples_y = []
x, y = 0.0, 0.0
exp_old = - 0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4)
for step in range(nsteps):
    if uniform:
        xnew = random.uniform(-1.0, 1.0)
        ynew = random.uniform(-1.0, 1.0)
    else:
        xnew, ynew = gauss_cut(), gauss_cut()
    exp_new = - 0.5 * (xnew ** 2 + ynew ** 2) - alpha * (xnew ** 4 + ynew ** 4)
    if not uniform:
        exp_new /= truncnorm.pdf(xnew, -1.0, 1.0) * truncnorm.pdf(ynew, -1.0, 1.0) / minVal ** 2.0
    if random.uniform(0.0, 1.0) < math.exp(exp_new - exp_old):
        x = xnew
        y = ynew
        exp_old = exp_new
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A3_1')
if uniform:
    pylab.savefig('plot_A3_1.png')
else:
    pylab.savefig('plot_A3_1_gauss.png')
pylab.show()
