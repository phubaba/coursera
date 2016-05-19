import random, numpy, pylab, math

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

def analyticQ(d):
    return V_sph(d)/V_sph(d-1)

d = 200

x = [0] * (d - 1)

deltas = .25, #0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.00
n_trials = 4000000*5

old_radius_square = 0

dsamples = []
for delta in deltas:
    n_hits = 0
    n_accept = 0
    for i in range(n_trials):
        k = random.randint(0, d - 2)
        x_old_k = x[k]
        x_new_k = x_old_k + random.uniform(-delta, delta)
        new_radius_square = old_radius_square + x_new_k ** 2. - x_old_k ** 2.
        if new_radius_square < 1.0:
            x[k] = x_new_k
            old_radius_square = new_radius_square
            n_accept+=1
        alpha = random.uniform(-1, 1)
        if old_radius_square + alpha**2 < 1.0:
            n_hits += 1
            dsamples.append(numpy.array(x + [alpha]))
           
    print 'for delta: ', delta, 'got unit-disk acceptance rate: ', (n_accept + 0.) / (n_trials + 0.), 'Sample Q(%s) = %s, Analytic Q(%s) = %s' % (d, 2 * float(n_hits)/float(n_trials), d, analyticQ(d))

    rvalues = [numpy.sqrt(numpy.sum(dsample ** 2.)) for dsample in dsamples]
    minr, maxr = min(rvalues), max(rvalues)
    pylab.hist(rvalues, 100, normed = 'True')
    x = numpy.linspace(minr, maxr, 100)
    y = d * x ** (d-1)
    pylab.plot(x, y, c='red', linewidth=2.0)
    pylab.title('Theoretical Radius distribution for d = %s and \
        \nnormalized histogram for %s samples' % (d, str(len(rvalues))), fontsize = 18)
    pylab.xlabel('$x$', fontsize = 30)
    pylab.ylabel('$\pi(x)$', fontsize = 30)
    pylab.savefig('radiusdistd%s.png' % d)
    pylab.show()

    
