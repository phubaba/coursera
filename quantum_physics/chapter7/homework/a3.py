import math, pylab

import math, random, pylab
import numpy

import math, random, pylab

def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

def pi_two_bosons(x, beta):
    pi_x_1 = math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta / 2.0))
    pi_x_2 = math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta))
    weight_1 = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    weight_2 = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))
    pi_x = pi_x_1 * weight_1 + pi_x_2 * weight_2
    return pi_x

def levy_harmonic_path(k, beta):
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

betas = [.1, .25, 1, 2.5, 5]
nsteps = 5000
inState1s = []
inState2s = []
for beta in betas:
    inState1 = 0
    inState2 = 0
    low = levy_harmonic_path(2, beta)
    high = low[:]
    data = []
    for step in xrange(nsteps):
        # move 1
        if low[0] == high[0]:
            k = random.choice([0, 1])
            low[k] = levy_harmonic_path(1, beta)[0]
            high[k] = low[k]
            inState1+=1
        else:
            low[0], low[1] = levy_harmonic_path(2, beta)
            high[1] = low[0]
            high[0] = low[1]
            inState2+=1
        data += low[:]
        # move 2
        weight_old = (rho_harm_1d(low[0], high[0], beta) *
                    rho_harm_1d(low[1], high[1], beta))
        weight_new = (rho_harm_1d(low[0], high[1], beta) *
                    rho_harm_1d(low[1], high[0], beta))
        if random.uniform(0.0, 1.0) < weight_new / weight_old:
            high[0], high[1] = high[1], high[0]

    inState1s.append(inState1)
    inState2s.append(inState2)

def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

fract_two_cycles = [z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta)) for beta in betas]
fract_one_cycle = [z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta)) for beta in betas]

# graphics output

pylab.plot(betas, map(lambda x: float(x)/float(nsteps), inState1s), label='State 1')
pylab.plot(betas, map(lambda x: float(x)/float(nsteps), inState2s), label='State 2')
pylab.plot(betas, fract_one_cycle, label='State 1 analytic')
pylab.plot(betas, fract_two_cycles, label='State 2 analytic')

pylab.xlabel('Beta', fontsize=16)
pylab.ylabel('$\pi$(state i)', fontsize=16)
pylab.title('Probability Of Being In State', fontsize=16)
pylab.legend(loc='upper right')
pylab.savefig('a3.png')
pylab.show()
