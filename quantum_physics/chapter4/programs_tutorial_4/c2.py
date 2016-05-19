import random, numpy, pylab, math, pandas

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

def analyticQ(d):
    return V_sph(d)/V_sph(d-1)

d_max = 20
delta = .25
n_trial_counts = 6
initial_trial = 1
trial_mult = 10

sample_count = 10



n_trial = initial_trial


trials = []
analytic_v_sph = [V_sph(d_max)] * n_trial_counts

mean_v_sphs = []
mean_error_sphs = []
  
for n_trial_count in xrange(n_trial_counts):
    trials.append(n_trial)
    subtrials = []
    for sample in xrange(sample_count):
        qvalues = [2]
        for d in xrange(2, d_max+1):
            x = [0] * (d - 1)

            old_radius_square = 0
            n_hits = 0
            n_accept = 0
            for i in range(n_trial):
                k = random.randint(0, d - 2)
                x_old_k = x[k]
                x_new_k = x_old_k + random.uniform(-delta, delta)
                new_radius_square = old_radius_square + x_new_k ** 2. - x_old_k ** 2.
                if new_radius_square < 1.0:
                    x[k] = x_new_k
                    old_radius_square = new_radius_square
                    n_accept+=1
                alpha = random.uniform(-1, 1)
                if old_radius_square + alpha**2 < 1.0:
                    n_hits += 1

            qvalue = 2 * float(n_hits)/float(n_trial)
            qvalues.append(qvalue)
        subtrials.append(numpy.prod(qvalues))
    
    mean_v_sph = numpy.mean(subtrials)
    print n_trial, subtrials
    mean_v_sph_sq = numpy.mean(numpy.array(subtrials) ** 2)
    mean_v_sphs.append(mean_v_sph)
    mean_error_sphs.append(((mean_v_sph_sq - mean_v_sph ** 2)/sample_count) ** .5)
    
                    
    n_trial = n_trial * trial_mult

mean_v_sphs = numpy.array(mean_v_sphs)
analytic_v_sph = numpy.array(analytic_v_sph)
difference = numpy.abs(mean_v_sphs - analytic_v_sph)
mean_error_sphs = numpy.array(mean_error_sphs)
trials = numpy.array(trials)

data = numpy.vstack([mean_v_sphs, analytic_v_sph, mean_error_sphs, difference]).T

print pandas.DataFrame(data, trials, ["Mean V_sph", "Analytic V_sph", "Mean Error", "Abs Diff"])




