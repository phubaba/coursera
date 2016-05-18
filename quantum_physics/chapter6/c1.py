import math, random, pylab
import os, numpy

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

def show_path(x, step, B):
    path = x + [x[0]]
    #y_axis = range(len(x) + 1)
    y_axis = numpy.linspace(0, B, len(path))
    pylab.plot(path, y_axis, 'bo-', label='new path')
    pylab.legend()
    pylab.xlim(-2.5, 7.5)
    pylab.xlabel('$x$', fontsize=14)
    pylab.ylabel('$B$', fontsize=14)
    pylab.title('Naive path integral Monte Carlo, step %i' % step)
    pylab.savefig('b1_path_snapshot_%05i.png' % step)
    pylab.clf()

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x

def levy_free_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        x_mean = (dtau_prime * x[k - 1] + dtau * xend) / \
                 (dtau + dtau_prime)
        sigma = math.sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
        x.append(random.gauss(x_mean, sigma))
    return x

def V(x, cubic, quartic):
    pot = x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4
    return pot

def V_anharm(x, cubic, quartic):
    pot = cubic * x ** 3 + quartic * x ** 4
    return pot

levy_path = True

beta = 20.
N = 100
dtau = beta / N
nCut = 4
if nCut>=N:
    nCut = N-1
delta = 1.0
n_steps = 100000
x = [0.0] * N
data = []

sigma = 1.0 / math.sqrt( 2.0 * math.tanh( beta / 2.0))
cubic = -1.
quartic = 1.
vToUse = V_anharm if levy_path else V
pathFuncToUse = levy_harmonic_path if levy_path else levy_free_path
current_weight = math.exp(sum(-vToUse(a, cubic, quartic) * dtau for a in x))

accepted = 0
for step in range(n_steps):
    x_possible = x[:]
    x_possible = pathFuncToUse(x_possible[0], x_possible[nCut], dtau, nCut) + x_possible[(nCut) : ]

    Trotter_weight = math.exp(sum(-vToUse(a, cubic, quartic) * dtau for a in x_possible))
    if random.uniform(0.0, 1.0) < Trotter_weight / current_weight:
        accepted += 1
        x = x_possible[:]
        current_weight = Trotter_weight

    x = x[1:] + x[:1]

    if step % max(1, int(N/4.)) == 0:
        k = random.randint(0, N - 1)
        data.append(x[k])

print accepted/float(n_steps)


show_path(x, step, beta)

pylab.hist(data, normed=True, bins=100, label='QMC')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='harmonic analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.title('levy_anharmonic_path (beta=%s, N=%i, cubic=%s, quartic=%s)' % (beta, N, cubic, quartic))
pylab.xlim(-2, 2)
if levy_path:
    pylab.savefig('plot_C1_beta%s_levy_path.png' % beta)
else:
    pylab.savefig('plot_C1_beta%s_levy_free.png' % beta)
pylab.show()
