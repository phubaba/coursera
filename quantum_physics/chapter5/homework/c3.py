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

def Energy_pert(n, cubic, quartic):
    return n + 0.5 - 15.0 / 4.0 * cubic **2 * (n ** 2 + n + 11.0 / 30.0) \
         + 3.0 / 2.0 * quartic * (n ** 2 + n + 1.0 / 2.0)

def Z_pert(cubic, quartic, beta, n_max):
    Z = sum(math.exp(-beta * Energy_pert(n, cubic, quartic)) for n in range(n_max + 1))
    return Z

zdat = []
for quartic in [.001, .01, .1, .2, .3, .4, .5]:
    x_max = 5.0
    cubic = -quartic
    nx = 100
    dx = 2.0 * x_max / (nx - 1)
    x = [i * dx for i in range(-(nx - 1) / 2, nx / 2 + 1)] 
    beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
    beta     = 2.0 ** 1                      # actual value of beta (power of 2)
    rho = rho_anharmonic_trotter(x, beta_tmp, cubic, quartic)  # density matrix at initial beta
    rhoharmonic = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        rhoharmonic = numpy.dot(rhoharmonic, rhoharmonic)
        rhoharmonic *= dx
        beta_tmp *= 2.0

    Z = sum(rho[j, j] for j in range(nx + 1)) * dx
    try:
        Zcompare = Z_pert(cubic, quartic, beta, nx)
    except:
        Zcompare = numpy.nan
    zdat.append((quartic, cubic, Z, Zcompare))

for quartic, cubic, z_i, zcomp_i in zdat:
    print 'Cubic: %.2f, Quartic: %.2f, Z: %.2f, Zcomp: %.2f' % (cubic, quartic, z_i, zcomp_i)
