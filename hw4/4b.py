import random
import numpy
import math

def sample(n):
    samples = []
    for i in range(n):
        x = random.random()
        if x < 0.2:
            new_sample = numpy.random.normal(1.0, 5.0)
        elif x < 0.5:
            new_sample = numpy.random.normal(-2.0, 1.0)
        else:
            new_sample = numpy.random.normal(2.0, 3.0)
        samples.append(new_sample)
    return samples
            
def gaussian(mu, sig):
    return lambda x: (1.0/(sig*math.sqrt(2*math.pi))) * \
           math.exp(- (x-mu)**2/(2.0 * sig**2))

def f(x):
    f1 = gaussian(1.0,5.0)
    f2 = gaussian(-2.0,1.0)
    f3 = gaussian(2.0, 3.0)
    return 0.2 * f1(x) + 0.3 * f2(x) + 0.5 * f3(x)
    
def rejectionSample(n):
    count = 0
    samples = []
    g = gaussian(0.0, 5.1)
    while len(samples)<n:
        x = numpy.random.normal(0.0, 5.1)
        y = random.random()*2.25*g(x)
        if y < f(x):
            samples.append(x)
        count +=1
    print count
    return samples
    
def metropolisHastings(n, sig):
    accept = 0
    samples = []
    x = numpy.random.normal(0.0, 1.0)
    for i in range(n+500):
        y = numpy.random.normal(x, sig)
        alpha = min(1, f(y)/f(x))
        p = random.random()
        if p < alpha:
            samples.append(y)
            x = y
            accept += 1
        else:
            samples.append(x)
    print accept
    return samples[500::]
        
    
