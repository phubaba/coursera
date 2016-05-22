import random, math
import os
import pylab

def _show(S, L, T, nsteps, suffix, show):
    def x_y(k, L):
        y = k // L
        x = k - y * L
        return x, y

    conf = [[0 for x in range(L)] for y in range(L)]
    for k in range(N):
        x, y = x_y(k, L)
        conf[x][y] = S[k]

    pylab.imshow(conf, extent=[0, L, 0, L], interpolation='nearest')
    pylab.set_cmap('hot')
    pylab.title('Local_'+ str(T) + '_' + str(L))
    pylab.savefig('plot_A2_local_'+ str(T) + '_' + str(L)+ suffix + '_' + str(nsteps) + '.png')
    if show:
        pylab.show()

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

for L in [2, 4, 8, 16, 32, 64]:
    N = L * L
    nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
                (i // L) * L + (i - 1) % L, (i - L) % N)
                                        for i in range(N)}

    T = 2.27
    p  = 1.0 - math.exp(-2.0 / T)
    nsteps = 10000

    filename = 'data_local_'+ str(L) + '_' + str(T) + '_' + str(nsteps) + '.txt'
    if os.path.isfile(filename):
        f = open(filename, 'r')
        S = []
        for line in f:
            S.append(int(line))
        f.close()
        print 'Starting from file', filename
        _show(S, L, T, nsteps, 'init', False)
    else:
        S = [random.choice([1, -1]) for k in range(N)]
        print 'Starting from a random configuration'

    E = [energy(S, N, nbr)]
    for step in range(nsteps):
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            j = Pocket.pop()
            for l in nbr[j]:
                if S[l] == S[j] and l not in Cluster \
                       and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
        for j in Cluster:
            S[j] *= -1
        E.append(energy(S, N, nbr))
    print 'mean energy per spin:', sum(E) / float(len(E) * N)
    E_mean = sum(E) / len(E)
    E2_mean = sum(a ** 2 for a in E) / len(E)
    cv = (E2_mean - E_mean ** 2 ) / N / T ** 2
    print "L: %s, E_mean: %s, E2_mean: %s, cv: %s" % (L, E_mean, E2_mean, cv)

f = open(filename, 'w')
for a in S:
   f.write(str(a) + '\n')
f.close()
_show(S, L, T, nsteps, '', True)
