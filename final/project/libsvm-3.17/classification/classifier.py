from svmutil import *

m = svm_load_model('libsvm.model')

def classify(instance):
    global m
    return svm_predict([0], instance, m)