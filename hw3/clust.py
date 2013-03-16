# clust.py
# -------
# YOUR NAME HERE

import sys
import random
import utils
import numpy
import math
from autoclass_back import AutoClass
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#DATAFILE = "adults.txt"
DATAFILE = "adults-small.txt"

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



#computes mean-squared distance from points to clusters
#rs = r values, xs = x values (see notes)
def mean_squared(means, rlist, xs):
    tot = 0
    for n in range(len(xs)):
        for k in range(len(means)):
            tot += rlist[n][k]*utils.squareDistance(xs[n], means[k])
    return tot/len(xs)


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
    
def k_means(xs, numExamples,numClusters):
    #initializing of the means as randomly chosen members of the input
    means = random.sample(xs, numClusters)

    #initializing the membership variables
    #r_nk = 1 if example n is in cluster k, 0 if not
    rlist = []
#    for n in range(numExamples):
#        rlist.append([])
#        for k in range(numClusters):
#            rlist[n].append(0)

    #initialize the indicator matrix
    for n in range(numExamples):
        #find the index of the old mean
        rlist.append(zero_list(numClusters))
        #find the best cluster, i.e. that minimizes the L_2 norm
        k = utils.argmin_index(means, lambda y : utils.squareDistance(xs[n],y))
        rlist[n][k]=1        


    converged = False
    while not(converged):
        converged = True
        #we change this if any means get updated
        for n in range(numExamples):
            #find the index of the old mean
            k_old = numpy.argmax(rlist[n])
            rlist[n] = zero_list(numClusters)
            #find the best cluster, i.e. that minimizes the L_2 norm
            k = utils.argmin_index(means, lambda y : utils.squareDistance(xs[n],y))
            rlist[n][k]=1
            #as long as one datapoint changes clusters, we have failed to converge
            if not(k_old == k):
                converged = False
        #unit test
        assert checkMembership(rlist)
        for k in range(numClusters):
            means[k] = avg(rlist, xs, numExamples, k)

    print "---------"
        
   # for i in range(numClusters):
      #  print "mean of cluster ",i, " is ", means[i]

    print "mean_squared is ", mean_squared(means, rlist, xs)


#metrics for HAC:
def Distance(xs,ys):
    return math.sqrt(utils.squareDistance(xs,ys))

def min_metric(A,B):
    return min([Distance(a,b) for a in A for b in B])

def max_metric(A,B):
    return max([Distance(a,b) for a in A for b in B])

def mean_metric(A,B):
    dists = [Distance(a,b) for a in A for b in B]
    total = reduce(lambda x,y:x+y,dists)
    return total/float(len(A)*len(B))

def cent_metric(A,B):
    Asum = reduce(sum_vecs,A)
    Bsum = reduce(sum_vecs,B)
    return [a/float(len(A)) - b/float(len(B)) for a,b in zip(Asum,Bsum)]


def mean_of_cluster(clust):
    agg = reduce(sum_vecs, clust)
    return scale(1.0/len(clust), clust)
                 
def mean_squared_by_cluster(clusters):
    tot = 0
    for clust in clusters:
        clust_mean = mean_of_cluster(clust)
        for x in clust:
            tot += utils.squareDistance(x, clust_mean)
    return 1.0/len(cluster)*tot

#HIERARCHICAL AGGLOMERATIVE CLUSTERING
#d = 0: use min metric
#d = 1: use max metric
#d = 2: use mean metric
#d = 3: use cent method
def HAC(xs, numClusters, d=0):
    #the minimum distance metric
        
    clusters = []
    for x in xs:
        clusters.append([x])
    
    if(d==0):
        metric = min_metric
    if(d==1):
        metric = max_metric
    if(d==2):
        metric = mean_metric
    if(d==3):
        metric = cent_metric

    while len(clusters)>numClusters:
        #iterate through the pairs of clusters to find the pair
        #with indices ibest,jbest that are closest to each other
        ibest = 0
        jbest = 1
        mindist = metric(clusters[0],clusters[1])
        for i in range(len(clusters)):
            for j in range(i+1,len(clusters)):
                distance = metric(clusters[i],clusters[j])
                if(distance<mindist):
                    ibest = i
                    jbest = j
                    mindist = distance
        #remove clusters at index j, append to cluster at index i
        assert(ibest<jbest)
        jclust = clusters.pop(jbest)
        clusters[ibest] += jclust

    #not sure what the means of the final clusters are...
    
    print "sizes of clusters"
    for i in range(numClusters):
        print "%d: %d" % (i,len(clusters[i]))
    #print mean_squared_by_cluster(clusters)

    

    #need to lookup how to do this scatterplot thing
    #maketable(clusters)




#3dscatter
#---
#plots clusters in different colors in 3d!
def 3dscatter(clusters):
    colors = ['b','r','g','y']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(clusters)):
        cluster = clusters[i]
        xs = [x[0] for x in cluster]
        ys = [y[1] for y in cluster]
        zs = [z[2] for z in cluster]
        ax.scatter(xs,ys,zs,colors[i])
    plt.show()


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
    #printOutput(data,numExamples)

    # ==================== #
    # WRITE YOUR CODE HERE #
    # ==================== #

    #K-Means clustering
    xs = data[:numExamples]

    #initializing the data, just so we don't have to carry around everything
    #might want to randomize...
    
    #print "k-means results ... "
    #for numClusters in range(1, 11):
     #   k_means(xs,numExamples,numClusters)
    print "HAC results"
    print "number of clusters is ", numClusters
    for i in range(4):
        print "using metric", i
        HAC(xs,numClusters,i)
    
#    autoclass = AutoClass(xs,numClusters)
#    clusters = autoclass.Cluster(10,0.01)
#    for i in range(numClusters):
#        print "%d: %d" %(i,len(clusters[i]))

    



if __name__ == "__main__":
    validateInput()
    main()
