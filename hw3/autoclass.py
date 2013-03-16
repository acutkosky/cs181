from random import random,choice
from math import exp,pi,sqrt

#
# Have two classes, one for probability distributions over a binary set a
# nd another for a single-variate Gaussian.
# We're just considering each attribute to be independent for a
# given cluster so we only need worry about single-variable Guassians I believe.
#



class BinaryFeature:
    def __init__(self):
        self.theta = random()
        
    def update(self,featurelist,probabilities):
        #expected size of this cluster
        Esize = reduce(lambda x,y:x+y,probabilities) 

        #expected number of things in this cluster with this attribute
        Efeature = reduce(lambda sum,i:sum+(featurelist[i]>0)*probabilities[i],range(len(probabilities)))
        
        #theta is the probability of having this attribute given that one is in this cluster
        self.theta = Efeature/Esize

    #the probability that x occurs 
    def prob(self,x):
        if(x>0):
            return self.theta
        return 1-self.theta

class ContinuousFeature:
    def __init__(self,mu=None):
        #initialize stuff somehow. probably should be done better later.
        self.mu = 2*random()-1.0
        self.sigma = 2*random()
        if(mu == None):
            self.mu = 2*random()-1.0
        else:
            self.mu = mu
        self.sigma = 10*random()+0.01

    def update(self,featurelist,probabilities):
        #expected size of this cluster
        Esize = reduce(lambda x,y:x+y,probabilities) 
        if(Esize == 0.0):
            self.mu = choice(featurelist)
            self.sigma = 10*random()
        else:
        #expected mu
            self.mu = (1/float(Esize))*reduce(lambda x,i:x+probabilities[i]*featurelist[i],range(len(probabilities)))

        #expected sigma
            self.sigma = sqrt((1/float(Esize))*reduce(lambda x,i:x+probabilities[i]*(featurelist[i]-self.mu)**2,range(len(probabilities))))

        if(self.sigma<0.01):
            self.sigma = 0.01
    def prob(self,x):
        assert self.sigma>=0.01
        return 1/float(self.sigma*sqrt(2)*pi) *exp(-(x-self.mu)**2/float(2*self.sigma**2))

class AutoClass:

    #we need the following fields for each cluster k  = 1 ... numClusters:
    # -------
    # for the continuous variables:
    # - a list mu_k representing the mean of the continuous variables 
    # - a (diagonal) "matrix" cov_k with one entry (the variance) [so it's really a list]
    #   for each continuous variable
    # - a conditional probability gamma[n][k] = P(cluster = k | data x_n, params)
    # -------
    # for the discrete variables:
    # - eN_1[k] = expected number of 1's in the cluster)
    # - eN_d1[d][k] = expected number of 1's for feature d in the cluster)
    # - eN_d0[d][k] = expected number of 0's for feature d in the cluster)
    # - theta_c[k] = probability of 1 for the cluster
    # - theta_d1[d][k] = conditional probability of feature d given outcome 1
                         #i.e. expected number of 1's for feature d / expected number of 1's
    # - theta_d0[d][k] = conditional probability of feature d given outcome 0
                         #i.e. expected number of 0's for feature d / expected number of 0's
        


    def __init__(self,xs,numClusters):
        
        self.numExamples = len(xs)
        self.numClusters = numClusters
        self.xs = xs #examples
        self.numFeatures = len(xs[0])

        #pi[k] should be the probability that a random element is in cluster k
        self.pi = [random() for x in range(numClusters)]
        tot = reduce(lambda x,y:x+y,self.pi)
        self.pi = [x/tot for x in self.pi]
 

        #For d attributes and k clusters we have dk distributions
        self.featureDists = []
        for d in range(self.numFeatures):
            self.featureDists.append([])
        self.gamma = []
        for i in range(len(xs)):
            self.gamma.append([float('inf')]*self.numClusters)

        for d in range(self.numFeatures):
            #ideally the type of probability distribution we use here
            #would be specified by the feature number
            #this can be done later; probably the continuous version
            #works ok for discrete things too.
            for k in range(self.numClusters):
                achoice = choice(xs)
                val = achoice[d]
                feature = ContinuousFeature(val)
                self.featureDists[d].append(feature)



    def Pxgiveny(self,xval,k):
        assert len(xval)==self.numFeatures
        #probability of an example xval in cluster k
        return reduce(lambda p,i: p*self.featureDists[i][k].prob(xval[i]),range(len(xval)))


    #E step
    #for all clusters k:
    
    #for continuous variables
    #-------------
    #gamma[n][k] = P(Y_n = k | x_n, theta) computed using Bayes rule:
    #            = P(X_n | Y_n = k) P(Y_n = k) / sum P(X_n | Y_n = k') p(Y_n = k')

    #for discrete variables
    #-------------
    # eN_1[k] = 0
    # eN_d1[d][k] = 0 for all attributes d
    # eN_d0[d][k] = 0 for all attributes [d]
    # for all examples n:
    # p_1 = theta_c[k] * prod_{attributes d} theta_d1[d][k]^{xs[n][d]} * (1-theta_d1[n][k])^{xs[n][d]}
    # p_0 = (1-theta_c[k]) * prod_{attributes d} theta_d0[d][k]^{xs[n][d]} (1-theta_d0[d][k])^{xs[n][d]}
    # cond = p_1/ (p_0+p_1)
    # eN_1[k] += cond
    # for all attributes d:
    #   if xs[n][d] == 1:
    #       eN_d1[d][k] += cond
    #       eN_d0[d][k] += 1- cond
    def Estep(self,threshold = 0.1):
        """ does the E-step. If none of the gamma values canges by more than threshold, then we have converged"""
        converged = True
        for n in range(self.numExamples):
            #compute probability that a given example occurs
            denominator = reduce(lambda x,y:x+y,[self.pi[k]*self.Pxgiveny(self.xs[n],k) for k in range(self.numClusters)])
            for k in range(self.numClusters):
                gamma_nk = self.pi[k]*self.Pxgiveny(self.xs[n],k)/float(denominator)
                if(abs(gamma_nk-self.gamma[n][k])>threshold):
                    converged = False
                self.gamma[n][k] = gamma_nk

        return converged

    def updateFeatureDist(self,d,k):
        featurelist = [xi[d] for xi in self.xs]
        probabilities = [self.gamma[n][k] for n in range(self.numExamples)]
        self.featureDists[d][k].update(featurelist,probabilities)

    #M step
    def Mstep(self,):
        #update the pi values
        for k in range(self.numClusters):
            self.pi[k] = reduce(lambda x,n:x+self.gamma[n][k],range(self.numExamples),0)/float(self.numExamples)

        #now we farm each feature off to its individual update function
        for d in range(self.numFeatures):
            for k in range(self.numClusters):
                self.updateFeatureDist(d,k)

    def Cluster(self,maxsteps = 1000,threshold = 0.1):
        """returns a list of cluster lists. That is, if there are k clusters, this function returns a list of k lists with the jth list containing element ranfomly relevant between players."""
        converged = False
        step = 0
        while(not converged and step<maxsteps): 
            converged = self.Estep(threshold)
            self.Mstep()
            step += 1
        self.Estep()

        cluster = []
        for n in range(self.numExamples):
            cluster.append([])
        for n in range(self.numExamples):
            cluster[self.gamma[n].index(max(self.gamma[n]))].append(self.x[n])

        return cluster

