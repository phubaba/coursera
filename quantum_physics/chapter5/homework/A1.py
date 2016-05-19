import random, math, pylab

x = 0.0
delta = 0.5
data = []

mathPi14th = math.pi ** .25
def psi_0(x):
    return (1 / mathPi14th)*math.exp( - (x ** 2) / 2)

baseDistTitle = 'Theoretical T->0 groud state wave function $\pi(x)$'
def dist(x):
    return psi_0(x) ** 2.


for k in range(50000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  dist (x_new) / dist(x):
        x = x_new 
    data.append(x)

pylab.hist(data, 100, normed = 'True', label='Sampled distribution')
x = [a / 10.0 for a in range(-50, 51)]
y = [dist(a) for a in x]
pylab.plot(x, y, c='red', linewidth=2.0, label='Analytical distribution')
pylab.title(baseDistTitle + ' and \
    \nnormalized histogram for '+str(len(data))+' samples', fontsize = 18)

legend = pylab.legend(loc='upper left', shadow=True)
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.frame = legend.get_frame()frame.set_facecolor('0.90')# Set the fontsize
for label in legend.get_texts():    label.set_fontsize('large')
for label in legend.get_lines():    label.set_linewidth(1.5)  # the legend line width

pylab.xlabel('$x$', fontsize = 30)
pylab.ylabel('$\pi(x)$', fontsize = 30)
pylab.savefig('plot_markov_gauss_a1.png')
pylab.show()
