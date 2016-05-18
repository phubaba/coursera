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

levy_path = True
levy_freeze = False

beta = 20.0
N = 2
dtau = beta / N
nCut = int(N/2.)
delta = 1.0
n_steps = 400000
x = [5.0] * N
data = []

sigma = 1.0 / math.sqrt( 2.0 * math.tanh( beta / 2.0))

for step in range(n_steps):
    if not levy_path:
        k = random.randint(0, N - 1)
        knext, kprev = (k + 1) % N, (k - 1) % N
        x_new = x[k] + random.uniform(-delta, delta)
        old_weight  = (rho_free(x[knext], x[k], dtau) *
                    rho_free(x[k], x[kprev], dtau) *
                    math.exp(-0.5 * dtau * x[k] ** 2))
        new_weight  = (rho_free(x[knext], x_new, dtau) *
                    rho_free(x_new, x[kprev], dtau) *
                    math.exp(-0.5 * dtau * x_new ** 2))
        if random.uniform(0.0, 1.0) < new_weight / old_weight:
            x[k] = x_new
    else:
        x = x[nCut:] + x[:nCut]  # reorganize
        if levy_freeze:
            xUse = x[0]
        else:
            xUse = random.gauss(0.0, sigma)

        x = levy_harmonic_path(xUse, xUse, dtau, N)

    if step % N == 0:
        k = random.randint(0, N - 1)
        data.append(x[k])


show_path(x, step, beta)

pylab.hist(data, normed=True, bins=100, label='QMC')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
if levy_path:
    pylab.title('levy_harmonic_path (beta=%s, N=%i)' % (beta, N))
else:
    pylab.title('naive_harmonic_path (beta=%s, N=%i)' % (beta, N))
pylab.xlim(-2, 2)
if levy_path:
    if levy_freeze:
        pylab.savefig('plot_B1_beta%s_levy_freeze.png' % beta)
    else:
        pylab.savefig('plot_B1_beta%s_levy.png' % beta)
else:
    pylab.savefig('plot_B1_beta%s.png' % beta)
pylab.show()
