import math, random, pylab
import numpy

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)

beta = 0.1
nsteps = 100000
low_1, low_2 = levy_harmonic_path(2)
x = {low_1:low_1, low_2:low_2}
data = []
distances = []
for step in xrange(nsteps):
    # move 1
    a = random.choice(x.keys())
    if a == x[a]:
        dummy = x.pop(a)
        a_new = levy_harmonic_path(1)[0]
        x[a_new] = a_new
    else:
        a_new, b_new = levy_harmonic_path(2)
        x = {a_new:b_new, b_new:a_new}
    # move 2
    (low1, high1), (low2, high2) = x.items()
    weight_old = rho_harm_1d(low1, high1, beta) * rho_harm_1d(low2, high2, beta)
    weight_new = rho_harm_1d(low1, high2, beta) * rho_harm_1d(low2, high1, beta)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        x = {low1:high2, low2:high1}
    distances.append(abs(x.keys()[1] - x.keys()[0]))

# graphics output

def prob_r_distinguishable(r, beta):
    sigma = math.sqrt(2.0) / math.sqrt(2.0 * math.tanh(beta / 2.0))
    prob = (math.sqrt(2.0 / math.pi) / sigma) * math.exp(- r ** 2 / 2.0 / sigma ** 2)
    return prob

pylab.hist(distances, normed=True, bins=100, label='Indistinguishable')

an_x = numpy.linspace(min(distances), max(distances), 100)
pylab.plot(an_x, [prob_r_distinguishable(an_x_i, beta) for an_x_i in an_x], label='Analytic Distinguishable')

pylab.xlabel('Absolute distance', fontsize=16)
pylab.ylabel('$\pi$', fontsize=16)
pylab.title('Distance between particles for beta%s' % beta, fontsize=16)
pylab.legend(loc='upper right')
pylab.savefig('a4.png')
pylab.show()
