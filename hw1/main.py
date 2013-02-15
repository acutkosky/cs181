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
def learn(dataset, pruneFlag, examples):
    learner = DecisionTreeLearner()
    learner.train( dataset)
    dtree = learner.dt
    if pruneFlag:
        prune(learner, dtree, examples)
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


def check_examples(dtree, examples,targetval):
    score = 0.0
    for example in examples:
        test = classify(dtree,example)
        check = example.attrs[targetval]
        if(test==check):
            score += 1.0
    return score/len(examples)

def crossvalidation(dataset,numexamples, pruneFlag, valSetSize):
    targetval = dataset.target
    valcumulativescore = 0.0
    learncumulativescore = 0.0
    for i in range(10):
        #divide up the data into chunks of 90% training, 10% validation
        learndata = dataset.examples[i*numexamples/10:(i-1)*numexamples/10+numexamples]
        #if you want to prune, further allocate pruning data
        if pruneFlag:
            training_data = learndata[valSetSize:]
            pruning_data = learndata[:valSetSize]
        else:
            training_data = learndata
        #set aside validation data
        validationdata = dataset.examples[(i-1)*numexamples/10+numexamples:(i)*numexamples/10+numexamples]
        old = dataset.examples
        #create a data set with examples from training_data
        dataset.examples = training_data
        #build the tree
        if pruneFlag:
            examples = pruning_data
        else:
            examples = training_data
        train = learn(dataset, pruneFlag, examples)
        #score the tree on the validation data
        valscore = check_examples(train, validationdata,targetval)
        learnscore = check_examples(train, learndata,targetval)
        valcumulativescore +=valscore
        learncumulativescore +=learnscore
        dataset.examples = old
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
      
    valscore,learnscore = crossvalidation(dataset,numexamples, pruneFlag, valSetSize)
    print "validation score: ",valscore," learningset score: ",learnscore

    
        
# ====================================
# WRITE CODE FOR YOUR EXPERIMENTS HERE
# ====================================

main()



