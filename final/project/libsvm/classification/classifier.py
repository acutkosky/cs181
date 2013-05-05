from svmutil import *
from pickle import load
#hi ashok

m = svm_load_model('libsvm.model')
print "m = ", m

def classify(instance):
    global m
    r =  svm_predict([0], [instance], m, "-q")
    return r[2][0][0]


print classify([0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0])




"""
#test the good plants
f = open("good_plants_small", 'r')
contents = load(f)[:1000]
f.close()

score = 0
tot = len(contents)
for x in contents:
    if classify(list(x))>0:
        score += 1
        print list(x)
print "percentage correct is " + str(score/float(tot))
"""

"""
#now to test the bad plants
f = open("bad_plants_small", 'r')
contents = load(f)
f.close()

score = 0
tot = len(contents)
for x in contents:
    if classify(list(x))<0:
        score += 1
print score/float(tot)
"""