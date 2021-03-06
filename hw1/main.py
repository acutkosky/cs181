# main.py
# -------
# Ashok Cutkosky and Tony Feng

import matplotlib.pyplot as plt
from pylab import *
import random
from dtree import *
import sys
from copy import deepcopy

class Globals:
    noisyFlag = False
    pruneFlag = False
    valSetSize = 0
    dataset = None


##Classify
#---------

def classify(learner, example):
    return learner.predict(example)

##Learn
#-------
def learn(dataset, prune,maxdepth):
    if (not dataset.use_boosting):
        learner = DecisionTreeLearner(pruningsize = prune)
    else:
        learner = BoostingLearner(dataset.num_rounds,maxdepth,[],[])
    learner.train( dataset)

    return learner

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'main.py', '-n', '-p', 5 ]) = { '-n':True, '-p':5 }"""
  args_map = {}
  curkey = None
  for i in xrange(1, len(args)):
    if args[i][0] == '-':
      args_map[args[i]] = True
      curkey = args[i]
    else:
      assert curkey
      args_map[curkey] = args[i]
      curkey = None
  return args_map

def validateInput(args):
    args_map = parseArgs(args)
    valSetSize = 0
    noisyFlag = False
    pruneFlag = False
    boostRounds = -1
    maxDepth = -1
    if '-n' in args_map:
      noisyFlag = True
    if '-p' in args_map:
      pruneFlag = True
      valSetSize = int(args_map['-p'])
    if '-d' in args_map:
      maxDepth = int(args_map['-d'])
    if '-b' in args_map:
      boostRounds = int(args_map['-b'])
    return [noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds]


def check_examples(train, examples,targetval):
    score = 0.0
    for example in examples:
        test = classify(train,example)
        check = example.attrs[targetval]
        if(test==check):
            score += 1.0
    return score/len(examples)

def crossvalidation(dataset,numexamples, pruneFlag, valSetSize,maxDepth):
    targetval = dataset.target
    valcumulativescore = 0.0
    learncumulativescore = 0.0
    if (not pruneFlag):
        valSetSize = 0
    for i in range(10):
        #divide up the data into chunks of 90% training, 10% validation
        learndata = dataset.examples[i*numexamples/10:(i-1)*numexamples/10+numexamples]
        training_data = learndata
        #set aside validation data
        validationdata = dataset.examples[(i-1)*numexamples/10+numexamples:(i)*numexamples/10+numexamples]
        old = deepcopy(dataset.examples)
        #create a data set with examples from training_data
        dataset.examples = training_data
        #build the tree

        train = learn(dataset, valSetSize,maxDepth)
        #score the tree on the validation data
        valscore = check_examples(train, validationdata,targetval)
        learnscore = check_examples(train, learndata,targetval)
        valcumulativescore +=valscore
        learncumulativescore +=learnscore
        dataset.examples = old
#        print train.dt
#        print "valscore: ",valscore,"learnscore: ",learnscore
#        exit()

    valcumulativescore /= 10
    learncumulativescore /= 10
    return valcumulativescore, learncumulativescore


def prune(learner, z, examples):
    #if it's a leaf, leave it alone
    if z.nodetype == DecisionTree.NODE:
        #get branches
        branches = z.branches
        #get the attribute
        attr = z.attr
        for (v, examples_i) in learner.split_by(attr, examples):
            #if there aren't any such examples, ignore that branch
            if len(examples_i)>0:
                prune(learner, branches[v], examples_i)
        #yz = majority class
        yz = learner.majority_value(examples)
        num_yz = learner.count(learner.dataset.target, yz, examples)
        tot = len(examples)
        t0_score = float(num_yz)/tot
        z_score = check_examples(z, examples, learner.dataset.target)
        #print z_score, t0_score
        #if the majority rule performs better, cut off the rest of the tree
        if z_score <= t0_score:
            z = DecisionTree(DecisionTree.LEAF, classification = yz)
  #          print "I pruned something!"
#        else:
 #           print "I didn't prune!"


def main(n, p, v, d, br):
    arguments = validateInput(sys.argv)
    noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds = arguments
    print noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds
    #noisyFlag = n
    #pruneFlag = p
    #valSetSize = v
    #maxDepth = d
    #boostRounds = br
    # Read in the data file
    
    if noisyFlag:
        f = open("noisy.csv")
    else:
        f = open("data.csv")

    data = parse_csv(f.read(), " ")
    dataset = DataSet(data)
    
    # Copy the dataset so we have two copies of it
    examples = dataset.examples[:]
    

    numexamples = len(examples)

    dataset.examples.extend(examples)
    dataset.max_depth = maxDepth
    if boostRounds != -1:
      dataset.use_boosting = True
      dataset.num_rounds = boostRounds
      
    valscore,learnscore = crossvalidation(dataset,numexamples, pruneFlag, valSetSize,maxDepth)
    return (valscore, learnscore)
    
        
# ====================================
# WRITE CODE FOR YOUR EXPERIMENTS HERE
# ====================================

valscore,learnscore =  main(False,False,0, 2, 30)
print "valscore: ",valscore," learnescore: ",learnscore


"""
xs = range(1, 16)
valscores_noiseless = []
learnscores_noiseless = []
for x in xs:
    a,b = main(False, False, 0, 1, x)
    valscores_noiseless.append(a)
    learnscores_noiseless.append(b)
print valscores_noiseless
print learnscores_noiseless



xs = range(1, 31)
valscores_noiseless = []
learnscores_noiseless = []
for x in xs:
    a,b = main(False, False, 0, 1, x)
    valscores_noiseless.append(a)
    #learnscores_noiseless.append(b)
print valscores_noiseless
#print learnscores_noiseless

valscores_noise = []
#learnscores_noise = []
for x in xs:
    a,b = main(True, False, 0, 1, x)
    valscores_noise.append(a)
#    learnscores_noise.append(b)

print valscores_noise
#print learnscores_noise


ax=plt.subplot(111)
ax.plot(xs, valscores_noiseless, 'b-', linewidth = 2.5, label = "Validation scores, noiseless")
ax.plot(xs, valscores_noise, 'g-', linewidth = 2.5, label = "Validation scores, noisy")
ax.legend()
ax.set_xlabel("Boosting set size", fontsize = 16)
ax.set_ylabel("Score", fontsize = 16) 
ax.set_title("Boosting Set Size and Performance", fontsize = 20)
plt.show()
"""

"""
valscore,learnscore = main(False,False,0)
print "Validation set score: ",valscore," Learning set score: ",learnscore

xs = range(1, 81)
valscores_noiseless = []
learnscores_noiseless = []
for x in xs:
    a,b = main(False, True, x)
    valscores_noiseless.append(a)
    learnscores_noiseless.append(b)
print valscores_noiseless
print learnscores_noiseless

valscores_noise = []
learnscores_noise = []
for x in xs:
    a,b = main(True, True, x)
    valscores_noise.append(a)
    learnscores_noise.append(b)

print valscores_noise
print learnscores_noise


ax=plt.subplot(111)
ax.plot(xs, valscores_noiseless, 'b-', linewidth = 2.5, label = "Validation scores, noiseless")
ax.plot(xs, learnscores_noiseless, 'r-', linewidth = 2.5, label = "Learning scores, noiseless")
ax.plot(xs, valscores_noise, 'g-', linewidth = 2.5, label = "Validation scores, noisy")
ax.plot(xs, learnscores_noise, 'm-', linewidth = 2.5, label = "Learning scores, noisy")
ax.legend()
ax.set_xlabel("boosting rounds", fontsize = 16)
ax.set_ylabel("Score", fontsize = 16) 
ax.set_title("Boosting Rounds and Performance", fontsize = 20)
plt.show()
    


"""
