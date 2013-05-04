from svmutil import *
import random
from pickle import load

svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

data_set = []
validation_set = []
f = open("good_plants_small", 'r')
contents = load(f)
print len(contents)
random.shuffle(contents)
good_data = contents[50000:]
good_validation = contents[50000:]
f.close()

f = open("bad_plants_small", 'r')
contents = load(f)
print len(contents)
random.shuffle(contents)
bad_data = contents[:125000]
bad_validation = contents[125000:]
f.close()

for x in good_data:
    data_set.append(list(x))
for x in bad_data:
    data_set.append(list(x))
for x in good_validation:
    validation_set.append(list(x))
for x in bad_validation:
    validation_set.append(list(x))
    

labels = [1]*len(good_data)
labels += [0] * len(bad_data)

test_labels = [1] * len(good_validation)
test_labels += [0] * len(bad_validation)

prob = svm_problem(labels, data_set)


C = 5.0
gamma = 0
params = "-s 0 -t 2 -h 0 -g " + str(2**(gamma))  + " -c " + str(2**C)
model = svm_train(prob, params)

svm_save_model('libsvm.model', model)

listvals = svm_predict(test_labels, validation_set, model)

scores = [x[0] for x in listvals[2]]
bins = [0]*10

f = open('training_log.txt', 'w')
f.close()
#sort the dataset into ten groups
sort_set = [[], [], [], [], [], [], [], [], [], []]
res_set = [[], [], [], [], [], [], [], [], [], []]
for i in range(len(validation_set)):
    ind = int(scores[i]/ 0.3) + 5
    sort_set[ind].append(validation_set[i])
    res_set[ind].append(test_labels[i])
i = len(sort_set)-1
while i>= 0:
    f.write(str(len(sort_set[i])) + "\n")
    if len(sort_set[i]) == 0:
        del sort_set[i]
        del res_set[i]
    i -= 1

pred_results = []
for i in range(len(sort_set)):
    f.write("i = ", str(i))
    pred_results.append(svm_predict(res_set[i], sort_set[i], model))
f.write(pred_results)
f.close()
    



"""



C = 4.3
gamma = -1
params = "-s 0 -t 2 -g " + str(2**(gamma))  + " -c " + str(2**C) + "-h 0 -v 5"

scores = []
for i in range(7):
    print  "-------"
    print "C = ", C, "gamma = ", gamma
    param = "-s 0 -t 2 -h 0 -g "
    param += str(2**gamma)
    param += " -c "
    param += str(2**C)
    param += " -v 5"
    gamma += 1
    C += .7
    scores.append(svm_train(prob, param))
print scores

print "--------------------"

C = 4.3
gamma = -1
params = "-s 0 -t 2 -g " + str(2**(gamma))  + " -c " + str(2**C) + "-h 0 -v 5"

scores = []
ms = [] 
for i in range(10):
    print  "-------"
    print "C = ", C, "gamma = ", gamma
    param = "-s 0 -t 2 -h 0 -g "
    param += str(2**gamma)
    param += " -c "
    param += str(2**C)
    gamma += 1
    C += .7
    ms.append(svm_train(prob, param))
    scores.append(svm_predict(test_labels, validation_set, ms[i]))


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


