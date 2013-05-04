import plant_pics
import game_interface
from random import randint

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class MDP:
  def __init__(self):
    self.V = {}
    self.Visits = {}
    self.gamma = 0.5
    self.epsilon = 0.01
    self.visit_penalty = 0.1
    self.poison_penalty = 10
    for s in self.get_states():
      self.V[s] = -1
      self.R[s] = -1.0

  def R(s,a):
    if(abs(s[0])>20 or abs(s[1])>20):
      return -10
    return R[s]

  def T(a,s,s_prime):
    #let's go with 15 70 15 for now
    forward = 0.7
    side = 0.15


    if(a = NORTH):
      if(s_prime[1]-1 == s[1] and s_prime[0] = s[0]):
        return forward
      if(s_prime[1] == s[1] and abs(s_prime[0]-s[0])==1):
        return side

    if(a = SOUTH):
      if(s_prime[1]+1 == s[1] and s_prime[0] = s[0]):
        return forward
      if(s_prime[1] == s[1] and abs(s_prime[0]-s[0])==1):
        return side

    if(a = EAST):
      if(s_prime[0]-1 == s[0] and s_prime[1] = s[1]):
        return forward
      if(s_prime[0] == s[0] and abs(s_prime[1]-s[1])==1):
        return side

    if(a = EAST):
      if(s_prime[0]+1 == s[0] and s_prime[1] = s[1]):
        return forward
      if(s_prime[0] == s[0] and abs(s_prime[1]-s[1])==1):
        return side

    


  def Update(view):
    s = (view.GetXPos(),view.GetYPos())
    R[s] -= self.visit_penalty


  def MarkPoison(view):
    s = (view.GetXPos(),view.GetYPos())
    R[s] -= self.poison_penalty


  def valueiteration(self,state):
    notconverged = True
    V_prime = {}
    PI = {}
    Q = {}
    xval = state[0]
    yval = state[1]
    states = [(x,y) for x in range(max(-20,xval-5),min(21,xval+5)) for y in range(max(-20,yval-5),min(21,yval+5))]
    borderstates = [(x,y) for x in range(max(-20,xval-6),min(21,xval+6)) for y in range(max(-20,yval-6),min(21,yval+6))]
    
    while notconverged:
      for s in borderstates:
        V_prime[s] = self.V[s]
        Q[s] = {}
      for s in states:
          for a in range(0,4):
            summand = 0
            xmin = max(-20,s[0]-1)
            xmax = min(21,s[0]+1)
            ymin = max(-20,s[1]-1)
            ymax = min(21,s[1]+1)
            neighborstates = [(x,y) for x in range(xmin,xmax) for y in range(ymin,ymax)]

            for s_prime in neighborstates:
              summand += self.T(a,s,s_prime)*V_prime[s_prime]
            Q[s][a] = self.R(s,a) + self.gamma*summand

          PI[s] = 0
          max_q = None
          for a in range(0,4):
            if(max_q <= Q[s][a]):
              max_q = Q[s][a]
              PI[s] = a
          V[s] = max_q
      notconverged = False
      for s in states:
        if abs(V[s]-V_prime[s]) > self.epsilon:
          notconverged = True
      
    return PI

  def get_move(self,view):
    s = (view.GetXPos(),view.GetYPos())
    if(abs(s[0])>20 or abs(s[1])>20): #outside the box!
      return randint(0,3)

    PI = self.valueiteration(s)
    return PI[s]


  def get_states(self):
    return [(x,y) for x in range(-20,21) for y in range(-20,21)]





def get_move(view):
  plant_pics.update(view)
  return plant_pics.get_move(view)
