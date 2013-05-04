from PyML import *
from base import *
from classifiers import *
from clusterers import *
from containers import *
from datagetn import *
from demo import *
from evaluators import *
from feature_selection import *
from preproc import *
from utils import *

from pickle import load

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

L = ["1"]*len(good_data)
L += ["0"] * len(bad_data)

s = SVM()
s.train(data)
r = s.stratifiedCV(data, 5)
