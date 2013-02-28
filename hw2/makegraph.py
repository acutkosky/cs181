from pickle import load
from sys import argv
from matplotlib import pyplot

f = open(argv[1],"r")
data = load(f)
f.close()

epochs = range(1,len(data))
training = [1-x[0] for x in data[1:]]
validation = [1-x[1] for x in data[1:]]
pyplot.plot(epochs,training,label = "training data")
pyplot.plot(epochs,validation,label = "validataion data")
pyplot.legend()

if(len(argv)>2):
    pyplot.title(argv[2])

pyplot.show()
