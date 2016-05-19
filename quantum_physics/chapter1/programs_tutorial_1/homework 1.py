'''

author: Rob Forler, phubaba@gmail.com
run the script via python '.\homework 1.py' if on windows in the cmd line or python <filename> of linux

the script runs with a variety of defaults already set, you can do:

python '.\homework 1.py' --help

to find out the arguments

'''

import random
import math

def _test_n_steps(n_steps):
    if n_steps < 1:
        raise ValueError("n_steps must be greater than 0")
    if not isinstance(n_steps, int):
        raise ValueError("n_steps must be an integer")


def direct_sample_pi(n_steps=40000):
    '''
    evaluates pi using a direct sampling monte carlo
    n_steps is an integer > 0 indicating the number of samples to run
    '''
    _test_n_steps(n_steps)

    n_hits = 0
    for iter in range(n_steps):
        x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
        if x**2 + y**2 < 1.0:
            n_hits += 1
    return 4.0 * n_hits / float(n_steps)


def mcmc_sample_pi(n_steps=40000, delta=.1):
    '''
    evaluates pi using a markov chain monte carlo
    n_steps is an integer > 0 indicating the number mcmc steps to take

    returns pi, rejection rate
    '''
    _test_n_steps(n_steps)
    x, y = 1.0, 1.0
    n_hits = 0
    rejection_count = 0
    sample_path = []
    for i in range(n_steps):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
        else:
            rejection_count += 1
        if x**2 + y**2 < 1.0:
            n_hits += 1
            sample_path.append(1)
        else:
            sample_path.append(0)
    return 4.0 * n_hits / float(n_steps), (rejection_count + 0.) / (n_steps + 0.), sample_path

def calculatePIFromPath(sample_path):
    return 4.0 * numpy.mean(sample_path)

def data_bunch(sample_path):
    '''
    implements the size 2 data_bunch algorithm
    '''
    sample_path = numpy.array(sample_path)
    newX = (sample_path[::2] + sample_path[1::2]) / 2.
    return numpy.mean(sample_path), numpy.std(sample_path, ddof=1), newX

if __name__ == '__main__':
    '''
    run the homework questions

    run the script via python '.\homework 1.py' if on windows or python <filename> of linux
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_steps", type=int, default=4000,
                        help="number of samples in direct sample or number of steps in mcmc")
    parser.add_argument("--n_samples", type=int, default=100,
                        help="number of times to rerun the algorithms to come up with a standard error")
    parser.add_argument("--mcmc_delta", type=float, default=.01,
                        help="choose the mcmc delta size")
    args = parser.parse_args()
    print 'Running with n_steps: %s, n_samples: %s, mcmc delta: %0.3f' % (args.n_steps, args.n_samples, args.mcmc_delta)

    _test_n_steps(args.n_samples)

    direct_samples = []
    mcmc_samples = []
    mcmc_rejection_rates = []
    mcmc_samples_p5 = []
    mcmc_rejection_rates_p5 = []

    p5delta = 1.175 #found in an adhoc way by altering program input
    for count in xrange(args.n_samples):
        direct_sample = direct_sample_pi(args.n_steps)
        direct_samples.append(direct_sample)
        mcmc_sample, mcmc_rejection_rate, _ = mcmc_sample_pi(args.n_steps, delta=args.mcmc_delta)
        mcmc_samples.append(mcmc_sample)
        mcmc_rejection_rates.append(mcmc_rejection_rate)
        mcmc_sample_p5, mcmc_rejection_rate_p5, _ = mcmc_sample_pi(args.n_steps, delta=p5delta)
        mcmc_samples_p5.append(mcmc_sample_p5)
        mcmc_rejection_rates_p5.append(mcmc_rejection_rate_p5)

    import numpy
    #simply compare each value to math.pi to calculate the error
    error_direct = numpy.std([x-math.pi for x in direct_samples], ddof=1)
    error_mcmc = numpy.std([x-math.pi for x in mcmc_samples], ddof=1)
    error_mcmc_p5 = numpy.std([x-math.pi for x in mcmc_samples_p5], ddof=1)

    print "Q1. Direct Sampling PI Mean Estimate: %0.10f. Sample standard deviation: %0.10f" % (numpy.mean(direct_samples), error_direct)
    print "\n"
    print "Q2a. MCMC PI Mean Estimate: %0.10f. Sample standard deviation: %0.10f, Rejection Rate: %0.3f" % (
        numpy.mean(mcmc_samples), error_mcmc, numpy.mean(mcmc_rejection_rates))
    print "Q2b. Using the 1/2 rejection rate rule for delta = %.4f, we get MCMC PI Mean Estimate: %0.10f. Sample Standard deviation: %0.10f, Rejection Rate: %0.3f. Relative error improvement over chosen mcmc delta is %.2f" % (
        p5delta, numpy.mean(mcmc_samples_p5), error_mcmc_p5, numpy.mean(mcmc_rejection_rates_p5), error_mcmc/error_mcmc_p5)
    print "\n"

    #data bunch approach, generate 1 longer sample and bunch into smaller bunches
    N = args.n_steps * args.n_samples
    maxBunches = int(numpy.floor(numpy.log(N) / numpy.log(2)))
    newN = 2**maxBunches
    print "Q3. Running bunching approach with n_steps: %s, n_samples: 1, mcmc delta at '1/2' rule: %0.3f" % ( newN, p5delta)
    _, _, mcmc_sample_path = mcmc_sample_pi(newN, delta=args.mcmc_delta)

    means, variances = [], []
    for bunch_number in xrange(maxBunches):
        mean, variance, mcmc_sample_path = data_bunch(mcmc_sample_path)
        means.append(mean)
        variances.append(variance)

    print "Analyzing the variance as a function of the bunching interval. I do not, however, see a plateau in the variances as a function of the bunching interval."
    for count, variance in enumerate(reversed(variances)):
        print "%s, %.03f" % (2**count, variance)


