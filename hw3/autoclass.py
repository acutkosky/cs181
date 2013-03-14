


class AutoClass:
    #fields
    numExamples
    numClusters
    attr #number of attributes 
    
    #the examples
    xs

    

    #initialize Gaussian mixture variables
    means = random.sample(xs, numClusters)

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


    cov_mat = covariance(xs)

    #convergence theshold: when the thetas stop changing by at least
    #threshold, the algorithm ``convergences''
    threshold = 0.1

    #set this to be true during M step if we have converged
    converged = False

    #E step
    def Estep():
        for n in range(self.numExamples):
            denominator = reduce(lambda x,y:x+y,[self.pi[k]*self.Pxgiveny(self.x[n],k) for k in range(self.numClusters)])
            for k in range(numClusters):
                self.gamma[n][k] = self.pi[k]*self.Pxgiveny(self.x[n],k)/float(denominator)

    def updateFeatureDist(d,k):
        featurelist = [xi[d] for xi in self.x]
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

    def Cluster():
        while(NOT CONVERGENT): #not sure what this condition should be
            self.Estep()
            self.Mstep()
        self.Estep()

        cluster = [[]]*self.numClusters
        for n in range(self.numExamples):
            cluster[self.gamma[n].index(max(self.gamma[n]))].append(self.x[n])

            

