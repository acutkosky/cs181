


class AutoClass:

    def Estep():
        for n in range(self.numExamples):
            denominator = reduce(lambda x,y:x+y,[self.pi[k]*self.Pxgiveny(self.x[n],k) for k in range(self.numClusters)])
            for k in range(numClusters):
                self.gamma[n][k] = self.pi[k]*self.Pxgiveny(self.x[n],k)/float(denominator)




    def updateFeatureDist(d,k):
        featurelist = [xi[d] for xi in self.x]
        probabilities = [self.gamma[n][k] for n in range self.numExamples]
        self.featureDists[i][k].update(featurelist,probabilities)



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

            

