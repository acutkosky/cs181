import math
from random import *
import throw
import darts

# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.


Q = {}
ALPHA = 1.0
TAU = 15.0
GAMMA = 0.5
EPSILON_EXP = 0.05
TAU_EXP = 15.0

def start_game(gamma):
  global GAMMA 
  GAMMA = gamma
  states = darts.get_states()
  actions = darts.get_actions()
  for s in states:
    Q[s] = {}
    for a in actions:
      Q[s][a]=None

  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES)) 

def get_target(turns,s,a,s_prime):

  Q_learning(darts.R(s,a),s,a,s_prime,turns)
  
  #to_explore = ex_strategy_one()
  to_explore = ex_strategy_two(turns)


  actions = darts.get_actions()
  action = None
  if(to_explore):
    #explore
    action = choice(actions)
  else:
    #exploit
      max_q = None
      for a in Q[s_prime]:
        if(max_q<Q[s_prime][a]):
          max_q = Q[s_prime][a]
          action = a

      if(action == None):
        action = choice(actions)
  return action

  #if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
  
  #return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))


# Exploration/exploitation strategy one.
def ex_strategy_one():

  if(random() < EPSILON_EXP):
    return 1
  else:
    return 0



# Exploration/exploitation strategy two.
def ex_strategy_two(g):
  if(random() < math.exp((-g+1)/TAU_EXP)):
    return 1
  else:
    return 0



#lower the learning rate
def decay_alpha(g):
  return 0.1#ALPHA * math.exp(-(g)/TAU)

# The Q-learning algorithm:
def Q_learning(R,s,a,s_prime,turns):

  alpha = decay_alpha(turns)

  max_q = None
  for a in Q[s_prime]:
    max_q = max(max_q,Q[s_prime][a])
  if(max_q == None):
    max_q = 0.0
  if(Q[s][a] == None):
    Q[s][a] = 0.0
  Q[s][a] = Q[s][a]+alpha*(R+GAMMA*max_q-Q[s][a])
  
  

  return
