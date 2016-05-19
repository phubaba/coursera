import random

x, y = 0., 0.
deltas = 0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.00
n_trials = 4000000
for delta in deltas:
    n_hits = 0
    n_accept = 0
    for i in range(n_trials):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if (x + del_x)**2 + (y + del_y)**2 < 1.0:
            x, y = x + del_x, y + del_y
            n_accept+=1
        z = random.uniform(-1, 1)
        if x**2 + y**2 + z**2 < 1.0:
            n_hits += 1
    print 'for delta: ', delta, 'got unit-disk acceptance rate: ', (n_accept + 0.) / (n_trials + 0.), 'Q(3) = ', 2 * float(n_hits)/float(n_trials)
