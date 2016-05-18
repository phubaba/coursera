import random, math, pylab
from scipy import integrate
from scipy.stats import truncnorm

alpha = .5
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

normalization = truncnorm.pdf(1., -1.0, 1.0)
for step in range(nsteps):
    if step % 2 == 0:
        while True:
            if uniform:
                x = random.uniform(-1.0, 1.0)
            else:
                x = gauss_cut()
            p = one_dim_f(x, alpha)
            if not uniform:
                p = p/truncnorm.pdf(x, -1.0, 1.0)./normalization
            if random.uniform(0.0, 1.0) < p:
                break
    else:
        while True:
            if uniform:
                y = random.uniform(-1.0, 1.0)
            else:
                x = gauss_cut()
            p = one_dim_f(y, alpha)
            if not uniform:
                p = p/truncnorm.pdf(y, -1.0, 1.0)./normalization
            if random.uniform(0.0, 1.0) < p:
                break
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A2_1')
if uniform:
    pylab.savefig('plot_A2_1.png')
else:
    pylab.savefig('plot_A2_1_gauss.png')
pylab.show()
