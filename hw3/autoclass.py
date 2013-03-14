from random import random
from math import exp.pi,sqrt

#
# Have two classes, one for probability distributions over a binary set and another for a single-variate Gaussian.
# We're just considering each attribute to be independent for a given cluster so we only need worry about single-variable Guassians I believe.
#



class BinaryFeature:
    def __init__():
        self.theta = random()
    def update(featurelist,probabilities):
        #expected size of this cluster
        Esize = reduce(lambda x,y:x+y,probabilities) 

        #expected number of things in this cluster with this attribute
        Efeature = reduce(lambda sum,i:sum+(featurelist[i]>0)*probabilities[i],range(len(probabilities)))
        
        #theta is the probability of having this attribute given that one is in this cluster
        self.theta = Efeature/Esize


    def prob(x):
        if(x>0):
            return self.theta
        return 1-self.theta

class ContinuousFeature:
    def __init__():
        #initialize stuff somehow. probably should be done better later.
        self.mu = 2*random()-1.0
        self.sigma = 2*random()

    def update(featurelist,probabilities):
        #expected size of this cluster
        Esize = reduce(lambda x,y:x+y,probabilities) 

        #expected mu
        self.mu = (1/float(Esize))*reduce(lambda x,i:x+probabilities[i]*featurelist[i],range(len(probabilities)))

        #expected sigma
        self.sigma = sqrt((1/float(Esize))*reduce(lambda x,i:x+probabilities[i]*(featurelist[i]-self.mu)**2,range(len(probabilities))))

    def prob(x):
        return 1/float(self.sigma*sqrt(2)*pi) *exp(-(x-self.mu))**2/float(2*self.sigma**2)

class AutoClass:


    def __init__(xs,numClusters):
        
        self.numExamples = len(xs)
        self.numClusters = numClusters
        self.xs = xs
        self.numFeatures = len(xs[0])

        #pi[k] should be the probability that a random element is in cluster k
        self.pi = [random() for x in range(numClusters)]

        #For d attributes and k clusters we have dk distributions
        self.featureDists = [[]]*self.numFeatures
        for d in range(self.numFeatures):
            #ideally the type of probability distribution we use here would be specified by the feature number
            #this can be done later; probably the continuous version works ok for discrete things too.
            for k in range(self.numClusters):
                featureDists[d].append(ContinuousFeature())

    #fields
    #numExamples
    #numClusters
    #attr #number of attributes 
    
    #the examples
    #xs

    

    #initialize Gaussian mixture variables
    #means = random.sample(xs, numClusters)

    #computes the covariance of random variables x and y over data
    #mu_x, mu_y are their means
    def cov(x, y):
        mu_x = sum(x)/float(len(x))
        mu_y = sum(y)/float(len(y))
        return 1.0/(len(x)*len(y)) * sum([(a-mu_x)*(b-mu_y) for \
                                          a in x and b in y])
        
        

    #computes the ``total covariance matrix'' of the data
    def covariance(xs):
        xs_attrs[i] = [x[i] for x in xs]
        cov_mat = []
        for i in range(attr):
            for j in range(attr):
                cov_mat[i][j] = cov(xs_attrs[i], xs_attrs[j])


    #cov_mat = covariance(xs)

    #convergence theshold: when the thetas stop changing by at least
    #threshold, the algorithm ``convergences''
    #threshold = 0.1

    #set this to be true during M step if we have converged
    #converged = False



    def Pxgiveny(xval,k):
        assert len(xval)==self.numFeatures
        #probability of an example xval in cluster k
        return reduce(lambda p,i: p*self.featureDists[i][k].prob(xval[i]),range(len(xval)))


    #E step
    def Estep(threshold = 0.1):
        """ does the E-step. If none of the gamma values canges by more than threshold, then we have converged"""
        converged = True
        for n in range(self.numExamples):
            #compute probability that a given example occurs
            denominator = reduce(lambda x,y:x+y,[self.pi[k]*self.Pxgiveny(self.xs[n],k) for k in range(self.numClusters)])
            for k in range(numClusters):
                gamma_nk = self.pi[k]*self.Pxgiveny(self.xs[n],k)/float(denominator)
                if(abs(gamma_nk-self.gamma[n][k])>threshold):
                    converged = False
                self.gamma[n][k] = gamma_nk

        return converged

    def updateFeatureDist(d,k):
        featurelist = [xi[d] for xi in self.xs]
        probabilities = [self.gamma[n][k] for n in range self.numExamples]
        self.featureDists[i][k].update(featurelist,probabilities)

    #M step
    def Mstep():
        #update the pi values
        for k in range(self.numClusters):
            self.pi[k] = reduce(lambda x,n:x+self.gamma[n][k],range(self.numExamples),0)/float(self.numExamples)

        #now we farm each feature off to its individual update function
        for d in range(self.numFeatures):
            for k in range(self.numClusters):
                self.updateFeatureDist(d,k)

    def Cluster(maxsteps = 1000,threshold = 0.1):
        """returns a list of cluster lists. That is, if there are k clusters, this function returns a list of k lists with the jth list containing element ranfomly relevant between players."""
        converged = False
        step = 0
        while(not converged and step<maxsteps): 
            converged = self.Estep(threshold)
            self.Mstep()
            step += 1
        self.Estep()

        cluster = [[]]*self.numClusters
        for n in range(self.numExamples):
            cluster[self.gamma[n].index(max(self.gamma[n]))].append(self.x[n])

        return cluster

