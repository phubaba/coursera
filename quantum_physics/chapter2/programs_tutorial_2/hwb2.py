import random, pylab
import copy


def run_markov_chain(L, sigma, delta, n_steps):
    L = copy.deepcopy(L)
    samples = [copy.deepcopy(L)]
    sigma_sq = sigma ** 2
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
        box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
        if not (box_cond or min_dist < 4.0 * sigma_sq):
            a[:] = b
        samples.append(copy.deepcopy(L))
    return samples



sigma = 0.1197
delta = .1
n_runs = 2000000
L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

samples = run_markov_chain(L, sigma, delta, n_runs)
histo_data = [pos[0][0] for pos in samples]
pylab.hist(histo_data, bins=100, normed=True)
pylab.xlabel('x')
pylab.ylabel('frequency')
pylab.title('Markov sampling: x coordinate histogram (density eta=0.18)')
pylab.grid()
pylab.savefig('markov_disks_histo.png')
pylab.show()
