from svmutil import *

from pickle import load

svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

data_set = [] 
f = open("good_plants", 'r')
good_data = load(f)
f.close()

f = open("bad_plants", 'r')
bad_data = load(f)
f.close()

for x in good_data:
    data_set.append(list(x))
for x in bad_data:
    data_set.append(list(x))

labels = [1]*len(good_data)
labels += [0] * len(bad_data)

prob = svm_problem(labels, data_set)

C = 5.6
gamma = -1.2
params = "-s 0 -t 2 -g " + str(2**(gamma))  + " -c " + str(2**C)
model = svm_train(prob, params)


svm_save_model('libsvm.model', model)
"""
listvals = svm_predict(labels, data_set, model)
print max(listvals[2])

scores = [x[0] for x in listvals[2]]
bins = [0]*10
print scores

#sort the dataset into ten groups
sort_set = [[], [], [], [], [], [], [], [], [], []]
res_set = [[], [], [], [], [], [], [], [], [], []]
for i in range(len(data_set)):
    ind = int(scores[i]/ 0.3) + 5
    sort_set[ind].append(data_set[i])
    res_set[ind].append(labels[i])
for x in sort_set:
    print len(x)
pred_results = []
for i in range(10):
    print "i=", i
    pred_results.append(svm_predict(res_set[i], sort_set[i], model))
    print pred_results
    """
    

             
#param = svm_parameter('-t 0 -c 4 -b 1')
#model = svm_train(prob, param)
#print "model=", model
#model.predict([0,1,1,0,1,0,0,0,1])


"""

C = 5.6
gamma = -1.2
params = "-s 0 -t 2 -g " + str(2**(gamma))  + " -c " + str(2**C) + " -v 5"

scores = []
for i in range(10):
    print  "-------"
    print "C = ", C, "gamma = ", gamma
    param = "-s 0 -t 2 -g "
    param += str(2**gamma)
    param += " -c "
    param += str(2**C)
    param += " -v 5"
    gamma += 0.1
    C += 0.2
    scores.append(svm_train(prob, param))
print scores
 
avg1 = 0.0
for i in range(10):
    avg1 += svm_train(prob, params)
print avg1/10.0

C = 5.8
gamma = -1.1
params = "-s 0 -t 2 -g " + str(2**(gamma))  + " -c " + str(2**C) + " -v 5"

avg2 = 0.0
for i in range(10):
    avg2 += svm_train(prob,params)
print avg2/10.0
        """


