import random, math

paths = 100000

sigma = 0.20
L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
counter = 0
for t in xrange(paths):
    a = random.choice(L)
    while True:
        b = [random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma)]
        min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
        if min_dist > 4.0 * sigma ** 2:
            a[:] = b
            break
    if L[0][0] < .25 and L[0][1] < .25: 
        counter += 1


L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
counter2 = 0
for t in range(paths):
    a = random.choice(L)
    b = [random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma)]
    min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
    if min_dist > 4.0 * sigma ** 2:
        a[:] = b
    if L[0][0] < .25 and L[0][1] < .25: 
        counter2 += 1

import random, math

delta = 0.1
L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
counter3 = 0
for t in range(paths):
    a = random.choice(L)
    L.remove(a)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L)
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
    if not (box_cond or min_dist < 4.0 * sigma ** 2):
        L.append(b)
    else:
        L.append(a)

    if L[0][0] < .25 and L[0][1] < .25: 
        counter3 += 1
    

print counter/float(paths)
print counter2/float(paths)
print counter3/float(paths)

