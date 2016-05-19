import random, math
import copy

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return d_x**2 + d_y**2 
    
def run_markov_chain(L, sigma, delta, n_steps):
    L = copy.deepcopy(L)
    samples = [copy.deepcopy(L)]
    sigma_sq = sigma ** 2
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min(dist(b, c) for c in L if c != a)
        if not (min_dist < 4.0 * sigma_sq):
            a[:] = b
        samples.append(copy.deepcopy(L))
    return samples

N = 4
eta = 0.26
sigma = math.sqrt(eta / N / math.pi)
n_runs = 4
delta = .05

L = [[0.25, 0.25], [0.25, 0.75], [0.75, 0.25], [0.75, 0.75]]

configs =  run_markov_chain(L, sigma, delta, n_runs)
print configs
print

