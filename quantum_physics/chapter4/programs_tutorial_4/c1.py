import random, numpy, pylab, math

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

def analyticQ(d):
    return V_sph(d)/V_sph(d-1)

d_max = 200
delta = .25
n_trials = 40000


qvalues = [2]

for d in xrange(2, d_max+1):
    x = [0] * (d - 1)

    old_radius_square = 0
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

    qvalue = 2 * float(n_hits)/float(n_trials)
    qvalues.append(qvalue)
    print 'for delta: ', delta, 'got disk acceptance rate: ', (n_accept + 0.) / (n_trials + 0.), 'Sample Q(%s) = %s, Analytic Q(%s) = %s' % (d, qvalue, d, analyticQ(d))

print qvalues

print "V_sph(%s) = %s" % (d, numpy.prod(qvalues))
v_sph = numpy.cumprod(qvalues)
dims = numpy.arange(d_max) + 1
analytical_v_sph = map(V_sph, dims)
pylab.plot(dims, analytical_v_sph, c='red', linewidth=2.0, label='Analytical V_sph')
pylab.plot(dims, v_sph, c='blue', linewidth=2.0, label='MC V_sph')
pylab.title('V_sph by dim', fontsize = 18)
pylab.xlabel('dim', fontsize = 30)
pylab.ylabel('V_sph', fontsize = 30)
pylab.yscale('log')

legend = pylab.legend(loc='upper center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

pylab.savefig('v_sph_%s.png' % d)
pylab.show()
