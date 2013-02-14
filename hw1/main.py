# main.py
# -------
# YOUR NAME HERE

from dtree import *
import sys

class Globals:
    noisyFlag = False
    pruneFlag = False
    valSetSize = 0
    dataset = None


##Classify
#---------

def classify(decisionTree, example):
    return decisionTree.predict(example)

##Learn
#-------
def learn(dataset):
    learner = DecisionTreeLearner()
    learner.train( dataset)
    return learner.dt

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


def crossvalidation(dataset,numexamples):
    targetval = dataset.target
    valcumulativescore = 0.0
    learncumulativescore = 0.0
    for i in range(10):
        learndata =dataset.examples[i*numexamples/10:(i-1)*numexamples/10+numexamples]
        validationdata = dataset.examples[(i-1)*numexamples/10+numexamples:(i)*numexamples/10+numexamples]
        old = dataset.examples
        dataset.examples = learndata
        train = learn(dataset)
        valscore = 0.0
        for example in validationdata:
            test = classify(train,example)
            check = example.attrs[targetval]
            if(test==check):
                valscore+=1.0
        valscore = valscore/len(validationdata)
        learnscore = 0.0
        for example in learndata:
            test = classify(train,example)
            check = example.attrs[targetval]
            if(test==check):
                learnscore+=1.0
        learnscore = learnscore/len(learndata)
        valcumulativescore +=valscore
        learncumulativescore +=learnscore
        dataset.examples = old
    valcumulativescore /= 10
    learncumulativescore /= 10

    return valcumulativescore,learncumulativescore

def main():
    arguments = validateInput(sys.argv)
    noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds = arguments
    print noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds

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
      
    valscore,learnscore = crossvalidation(dataset,numexamples)
    print "validation score: ",valscore," learningset score: ",learnscore
# ====================================
# WRITE CODE FOR YOUR EXPERIMENTS HERE
    # ====================================

main()


    
