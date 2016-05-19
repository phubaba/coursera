import random, math
import pylab
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


def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

N = 4
eta = 0.26
sigma = math.sqrt(eta / N / math.pi)
n_runs = 4
delta = .25

L = [[0.25, 0.25], [0.25, 0.75], [0.75, 0.25], [0.75, 0.75]]

configs =  run_markov_chain(L, sigma, delta, n_runs)
print configs
print

show_conf(configs[-1], sigma, "Configuration with periodic boundary conditions", "4_disks.png")


