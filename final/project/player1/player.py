import plant_pics
import game_interface
from random import randint

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

BOX_SIZE = 15
INNER_BOX = 15

def direction(dir):
  if(dir == NORTH):
    print "NORTH"
  if(dir == WEST):
    print "WEST"
  if(dir == SOUTH):
    print "SOUTH"
  if(dir == EAST):
    print "EAST"

class MDP:
  def __init__(self):
    self.V = {}
    self.Rvals = {}
    self.Visits = {}
    self.gamma = 0.5
    self.epsilon = 0.001
    self.visit_penalty = 0.8
    self.poison_penalty = 10
    for s in self.get_states():
      self.V[s] = 0.0
      self.Rvals[s] = 10.0
    self.valueiteration((0,0))

  def R(self,s,a):
    #return 1.0/(abs(s[0])+abs(s[1])+1)
    if(abs(s[0])>BOX_SIZE or abs(s[1])>BOX_SIZE):
      return 0
    return self.Rvals[s]

  def T(self,a,s,s_prime):
    #let's go with 15 70 15 for now
    forward = 0.7
    side = 0.15


    if(a == NORTH):
      if(s_prime[1]-1 == s[1] and s_prime[0] == s[0]):
        return forward
      if(s_prime[1] == s[1] and abs(s_prime[0]-s[0])==1):
        return side

    if(a == SOUTH):
      if(s_prime[1]+1 == s[1] and s_prime[0] == s[0]):
        return forward
      if(s_prime[1] == s[1] and abs(s_prime[0]-s[0])==1):
        return side

    if(a == EAST):
      if(s_prime[0]-1 == s[0] and s_prime[1] == s[1]):
        return forward
      if(s_prime[0] == s[0] and abs(s_prime[1]-s[1])==1):
        return side

    if(a == WEST):
      if(s_prime[0]+1 == s[0] and s_prime[1] == s[1]):
        return forward
      if(s_prime[0] == s[0] and abs(s_prime[1]-s[1])==1):
        return side

    return 0


  def Update(self,view):
    s = (view.GetXPos(),view.GetYPos())
    if(s in self.Rvals):
      self.Rvals[s] *= self.visit_penalty
    else:
      print "OUTSIDE THE BOX!",s

  def MarkPoison(self,view):
    s = (view.GetXPos(),view.GetYPos())
    self.Rvals[s] -= self.poison_penalty


  def valueiteration(self,state):
    notconverged = True
    V_prime = {}
    PI = {}
    Q = {}
    local_size = 6
    xval = state[0]
    yval = state[1]
    states = [(x,y) for x in range(max(-BOX_SIZE,xval-local_size),min(BOX_SIZE+1,xval+local_size)) for y in range(max(-BOX_SIZE,yval-local_size),min(BOX_SIZE+1,yval+local_size))]
    borderstates = [(x,y) for x in range(max(-BOX_SIZE,xval-local_size-1),min(BOX_SIZE+1,xval+local_size+1)) for y in range(max(-BOX_SIZE,yval-local_size-1),min(BOX_SIZE+1,yval+local_size+1))]
    
    for s in states:
        Q[s] = {}
        #self.V[s] = 0
    while notconverged:
      for s in borderstates:
        V_prime[s] = self.V[s]

      for s in states:
          for a in range(0,4):
            summand = 0
            xmin = max(-BOX_SIZE,s[0]-1)
            xmax = min(BOX_SIZE+1,s[0]+2)
            ymin = max(-BOX_SIZE,s[1]-1)
            ymax = min(BOX_SIZE+1,s[1]+2)
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
          self.V[s] = max_q
      notconverged = False
      for s in states:
        if abs(self.V[s]-V_prime[s]) > self.epsilon:
          notconverged = True
      
    return PI

  def get_move(self,view):
    s = (view.GetXPos(),view.GetYPos())
    if(abs(s[0])>BOX_SIZE or abs(s[1])>BOX_SIZE): #outside the box!
      return randint(0,3)

    PI = self.valueiteration(s)
    return PI[s]


  def get_states(self):
    return [(x,y) for x in range(-BOX_SIZE,BOX_SIZE+1) for y in range(-BOX_SIZE,BOX_SIZE+1)]




mdp = MDP()

def get_move(view):
  global mdp
  mdp.Update(view)
  move = mdp.get_move(view)
  print "located at: "+str(view.GetXPos())+" "+str(view.GetYPos())
  print "and moving"
  direction(move)
  has_plant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  return (move,has_plant)
