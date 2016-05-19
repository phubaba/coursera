import random
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


total_runs = 3
sigma = 0.15
delta = 0.1
n_steps = 10**6
del_xy = .05
L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))
configurations = [conf_a, conf_b, conf_c]
for run in xrange(total_runs):
    print "Run %s" % run, "\n"
    x_vecs = run_markov_chain(L, sigma, delta, n_steps)
    hits = {conf_a: 0, conf_b: 0, conf_c: 0}
    for x_vec in x_vecs:
        #import pdb; pdb.set_trace()
        for conf in configurations:
            condition_hit = True
            for b in conf:
                condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in x_vec) < del_xy

                condition_hit *= condition_b
            if condition_hit:
                hits[conf] += 1

    for conf in configurations:
        print conf, hits[conf], "\n"


