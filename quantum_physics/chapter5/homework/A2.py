import random, math, pylab, numpy

beta = 5
plotRange = -8.
numSteps = 1000000
baseDistTitle = 'Theoretical Beta:%s wave function $\pi(x)$' % beta
delta = 0.5
data = []
x = 0.0
n = 0

beta = float(beta)

mathPi14th = math.pi ** .25
sqrt2 = math.sqrt(2.0)
def psi_n(x, n):
    if n == -1:
        return 0.0
    else:
        psi = [math.exp(-x ** 2 / 2.0) / mathPi14th]
        psi.append(sqrt2 * x * psi[0])
        for k in xrange(2, n + 1):
            psi.append(math.sqrt(2.0 / k) * x * psi[k - 1] -
                       math.sqrt((k - 1.0) / k) * psi[k - 2])
        return psi[n]

def e_n(n):
    return n + .5

def distquantum(x):
    tanhb2 = math.tanh(beta/2)
    return math.sqrt(tanhb2/math.pi) * math.exp(-x**2 * tanhb2)

def distclassic(x):
    return math.sqrt(beta/(2*math.pi)) * math.exp(-x**2 * beta / 2.)

for k in range(numSteps):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  (psi_n (x_new, n) / psi_n(x, n)) ** 2.:
        x = x_new 

    n_new = n + (1 if random.uniform(0.0, 1.0) > .5 else -1)

    if random.uniform(0.0, 1.0) < (psi_n (x, n_new) / psi_n(x, n)) ** 2. * math.exp(-beta * (e_n(n_new) - e_n(n))):
        n = n_new
    
    data.append((n, x))

pylab.hist([b[1] for b in data], 100, normed = 'True', label='Sampled distribution')
x = [a for a in numpy.linspace(-plotRange, plotRange, 150)]
pylab.plot(x, [distquantum(a) for a in x], c='red', linewidth=2.0, label='Quantum distribution')
pylab.plot(x, [distclassic(a) for a in x], c='green', linewidth=2.0, label='Classical distribution')
pylab.title(baseDistTitle + ' and \
    \nnormalized histogram for '+str(len(data))+' samples', fontsize = 18)

legend = pylab.legend(loc='upper left', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')
# Set the fontsize

for label in legend.get_texts():
    label.set_fontsize('medium')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

pylab.xlabel('$x$', fontsize = 30)
pylab.ylabel('$\pi(x)$', fontsize = 30)
strBeta = str(beta) 
pylab.savefig('plot_markov_gauss_a2_%s.png' % strBeta)
pylab.show()
