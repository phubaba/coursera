import math, numpy, pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

def V_anharmonic(x, cubic, quartic):
    return x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

def rho_anharmonic_trotter(grid, beta, cubic, quartic):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * (V_anharmonic(x, cubic, quartic) + V_anharmonic(xp, cubic, quartic))) \
                         for x in grid] for xp in grid])


x_max = 5.0
cubic = -1
quartic = 1
nx = 200
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-(nx - 1) / 2, nx / 2 + 1)] 
beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
beta     = 2.0 ** 2                      # actual value of beta (power of 2)
rho = rho_anharmonic_trotter(x, beta_tmp, cubic, quartic)  # density matrix at initial beta
rhoharmonic = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    rhoharmonic = numpy.dot(rhoharmonic, rhoharmonic)
    rhoharmonic *= dx
    beta_tmp *= 2.0

Z = sum(rho[j, j] for j in range(nx + 1)) * dx
pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]

fileToLoad = 'data_anharm_matrixsquaring_beta' + str(beta) + 'cubic_%s_quartic_%s.dat' % (cubic, quartic)
f = open(fileToLoad, 'w')
for j in range(nx + 1):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

Z2 = sum(rhoharmonic[j, j] for j in range(nx + 1)) * dx
pi_of_x_harmonic = [rhoharmonic[j, j] / Z2 for j in range(nx + 1)]

# graphics output
f, ax = pylab.subplots(2, sharex=True)
ax[0].plot(x, pi_of_x_harmonic, label='Harmonic')
ax[0].plot(x, pi_of_x, label='Anhormonic c=%s, q=%s' % (cubic, quartic))
ax[0].set_title('$\pi(x)$ for Trotter Approx Quantum Oscilliators with $\\beta = 2^{%i}$' % (math.log(beta, 2)))
vals = [V_anharmonic(x_i, 0, 0) for x_i in x]
ax[1].plot(x, [v/max(vals) for v in vals], label='V_harmonic scaled')
vals = [V_anharmonic(x_i, cubic, quartic) for x_i in x]
ax[1].plot(x, [v/max(vals) for v in vals], label='V_anharmonic scaled')
ax[1].set_title('Potentials for different oscillitors')

ax[0].set_ylabel('$\pi(x)$', fontsize=18)
ax[1].set_xlabel('$x$', fontsize=18)
ax[1].set_ylabel('$V(x)$', fontsize=18)


for subax in ax:
    legend = subax.legend(loc='upper left', shadow=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    # Set the fontsize

    for label in legend.get_texts():
        label.set_fontsize('medium')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line widt

pylab.savefig('plot-harmonic-px_c1_beta%s_cubic%s_quartic_%s.png' % (beta, cubic, quartic))
pylab.show()

