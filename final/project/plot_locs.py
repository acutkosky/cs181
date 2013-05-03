import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import colormaps as cmp
from random import random

thresh = -0.0898170135494
thresh = (1.0-thresh)/2.0

f = open("plant_locs")

points_dict = {}
xvals = []
yvals = []
for line in f:
    data = line.split()
    point = (int(data[0]),int(data[1]))
    score = 0
    if(data[2] == "T"):
        score = 1
    else:
        assert(data[2] == "P")
        score = -1
    if(point not in points_dict):
        points_dict[point]=[0,0]
#    score = 1
#    if(random()<thresh):
#        score = -1
    points_dict[point][0]+=score
    points_dict[point][1]+=1

f.close()

Z = []
prob = 0.0
tot = 0.0
for point in points_dict:
    if(point!=(0,0)):
        xvals.append(point[0])
        yvals.append(point[1])
        prob+=points_dict[point][0]
        tot += points_dict[point][1]
        Z.append(float(points_dict[point][0])/float(points_dict[point][1]))
prob /= tot
print "prob: ",prob
binvals = (max(xvals)-min(xvals),max(yvals)-min(yvals))

H, xedges,yedges = np.histogram2d(xvals,yvals,bins = binvals,weights = Z)
extent =[yedges[0],yedges[-1],xedges[-1],xedges[0]]
print len(Z)


lim = max([abs(x) for x in Z])

plt.imshow(H,extent=extent,interpolation='nearest',cmap=cmp.blue_yellow_red)
plt.clim(-lim,lim)
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()

# Generate some test data
