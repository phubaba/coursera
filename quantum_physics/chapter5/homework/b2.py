import math, random, pylab, os

def rho_free(x, y, beta):        # free off-diagonal density matrix
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

output_dir = 'snapshots_naive_harmonic_path'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def show_path(x, k, x_old, Accepted, step):
    path = x + [x[0]]
    y_axis = range(len(x) + 1)
    if Accepted:
        old_path = x[:]
        old_path[k] = x_old
        old_path = old_path + [old_path[0]]
        pylab.plot(old_path, y_axis, 'ro--', label='old path')
    pylab.plot(path, y_axis, 'bo-', label='new path')
    pylab.legend()
    pylab.xlim(-5.0, 5.0)
    pylab.xlabel('$x$', fontsize=14)
    pylab.ylabel('$\\tau$', fontsize=14)
    pylab.title('Naive path integral Monte Carlo, step %i' % step)
    pylab.savefig(output_dir + '/snapshot_%05i.png' % step)
    pylab.clf()

beta = 4.0
fileToLoad = 'data_harm_matrixsquaring_beta' + str(beta) + '.dat'
sampleCount = 10
N = 10                                                # number of slices
dtau = beta / N
delta = 1.0                                          # maximum displacement on one slice
n_steps = 1000000                                       # number of Monte Carlo steps
x = [random.uniform(-1.0, 1.0) for k in range(N)]    # initial path
show_path(x, 0, 0.0, False, 0)
results = []
for step in range(n_steps):
    k = random.randint(0, N - 1)                     # randomly choose slice
    knext, kprev = (k + 1) % N, (k - 1) % N          # next/previous slices
    x_old = x[k]
    x_new = x[k] + random.uniform(-delta, delta)     # new position at slice k
    old_weight  = (rho_free(x[knext], x_old, dtau) *
                   rho_free(x_old, x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x_old ** 2))
    new_weight  = (rho_free(x[knext], x_new, dtau) *
                   rho_free(x_new, x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x_new ** 2))
    if random.uniform(0.0, 1.0) < new_weight / old_weight:
        x[k] = x_new
        Accepted = True
    else:
        Accepted = False
    if step % sampleCount == 0:
        results.append(x[-1])
    #show_path(x, k, x_old, Accepted, step + 1)

def read_file(filename):
    list_x = []
    list_y = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            list_x.append(float(x))
            list_y.append(float(y))
    f.close()
    return list_x, list_y

trotterx, trottery = read_file(fileToLoad)

# graphics output

pylab.hist(results, 100, normed = 'True', label='Path Sampled')
pylab.plot(trotterx, trottery, label='Trotter Approximation')
pylab.title('$\pi(x)$ for quantum harmonic oscilliator with $\\beta = 2^{%i}$' % math.log(beta, 2))
pylab.xlabel('$x$', fontsize=18)
pylab.ylabel('$x\'$', fontsize=18)

legend = pylab.legend(loc='upper left', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')
# Set the fontsize

for label in legend.get_texts():
    label.set_fontsize('medium')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line widt

pylab.savefig('plot-harmonic-px_b2_beta%s.png' % beta)
pylab.show()
