# clust.py
# -------
# YOUR NAME HERE

import sys
import random
import utils
import numpy

DATAFILE = "adults.txt"

#validateInput()

def validateInput():
    if len(sys.argv) != 3:
        return False
    if sys.argv[1] <= 0:
        return False
    if sys.argv[2] <= 0:
        return False
    return True


#-----------


def parseInput(datafile):
    """
    params datafile: a file object, as obtained from function `open`
    returns: a list of lists

    example (typical use):
    fin = open('myfile.txt')
    data = parseInput(fin)
    fin.close()
    """
    data = []
    for line in datafile:
        instance = line.split(",")
        instance = instance[:-1]
        data.append(map(lambda x:float(x),instance))
    return data


def printOutput(data, numExamples):
    for instance in data[:numExamples]:
        print ','.join([str(x) for x in instance])

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def main():
    # Validate the inputs
    if(validateInput() == False):
        print "Usage: clust numClusters numExamples"
        sys.exit(1);

    numClusters = int(sys.argv[1])
    numExamples = int(sys.argv[2])

    #Initialize the random seed
    
    random.seed()

    #Initialize the data

    
    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"


    data = parseInput(dataset)
    
    
    dataset.close()
    printOutput(data,numExamples)

    # ==================== #
    # WRITE YOUR CODE HERE #
    # ==================== #

    #K-Means clustering
    xs = data[:numExamples]

    #initializing the data, just so we don't have to carry around everything
    #might want to randomize...
    
    #initializing of the means as randomly chosen members of the input
    means = random.sample(xs, numClusters)

    #initializing the membership variables
    #r_nk = 1 if example n is in cluster k, 0 if not
    rlist = []
    for n in range(numExamples):
        rlist.append([])
        for k in range(numClusters):
            rlist[n].append(0)

    #initializes a list of k zeros
    def zero_list(k):
        return [0]*k

    #a unit test to make sure membership is correct: sum_k r_{nk} = 1 for all n
    def checkMembership(rlist):
        for x in rlist:
            if sum(x) != 1:
                return False
        return True

    #scales list v by a
    def scale(a, v):
        return [a*x for x in v]

    #sums two vectors
    def sum_vecs(v1, v2):
        n = len(v1)
        if not(n== len(v2)):
            raise ValueError
        new_vec = []
        for i in range(n):
            new_vec.append(v1[i] + v2[i])
        return new_vec

    #calculating the mean of a number of vectors
    #rs = r values, xs = x values (see notes)
    def avg(rlist, xs, numExamples, k):
        weight = 0
        #compute the weighting factor
        for n in range(numExamples):
            weight += rlist[n][k]
        #compute the weighted sum (numerator of formula)
        aggregate = zero_list(len(xs[0]))
        for n in range(numExamples):
            aggregate = sum_vecs(aggregate, scale(rlist[n][k],xs[n]))
        try:
            return scale(1.0/weight, aggregate)
        except: #nothing in this cluster, go to random point
            return random.sample(xs, 1)
    

    converged = False
    while not(converged):
        converged = True
        #we change this if any means get updated
        for n in range(numExamples):
            #find the index of the old mean
            k_old = numpy.argmax(rlist[n])
            rlist[n] = zero_list(numClusters)
            #find the best cluster, i.e. that minimizes the L_2 norm
            k = utils.argmin_index(means, lambda y : utils.squareDistance(data[n],y))
            rlist[n][k]=1
            #as long as one datapoint changes clusters, we have failed to converge
            if not(k_old == k):
                condition = False
        #unit test
        assert checkMembership(rlist)
        for k in range(numClusters):
            means[k] = avg(rlist, xs, numExamples, k)

    print "---------"
     
    for i in range(numClusters):
        print "mean of cluster ",i, " is ", means[i]

    #computes mean-squared distance from points to clusters
    #rs = r values, xs = x values (see notes)
    def mean_squared(means, rlist, xs):
        tot = 0
        for n in range(len(xs)):
            for k in range(len(means)):
                tot += rlist[n][k]*utils.squareDistance(xs[n], means[k])
        return tot

    print "mean_squared is ", mean_squared(means, rlist, xs)







if __name__ == "__main__":
    validateInput()
    main()
