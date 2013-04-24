

# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

from throw import CENTER, INNER_RING, FIRST_PATCH, MIDDLE_RING, SECOND_PATCH, OUTER_RING, MISS,NUM_WEDGES

# make pi global so computation need only occur once
PI = {}
EPSILON = .001


# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  #for ele in PI:
    #print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):

  return PI[score]

# define transition matrix/ function
def T(a, s, s_prime):
  # takes an action a, current state s, and next state s_prime
  # returns the probability of transitioning to s_prime when taking action a in state s

  #so let's iterate over the possible places on the board we will hit and add up the ones that give the right score reduction

  if(s_prime>s):
    return 0.0

  if(s == 0 and s_prime == 0):
    return 1.0

  regions = {CENTER:0, INNER_RING:1, FIRST_PATCH:2, MIDDLE_RING:3, SECOND_PATCH:4,OUTER_RING:5,MISS:6}


  actions = darts.get_actions()

  score_diff = s-s_prime
  prob = 0.0
  for ap in actions:
    prob_ap = 0.0
    if(throw.location_to_score(ap) == score_diff):
      diff = int(a.wedge-ap.wedge)

      diff = diff% NUM_WEDGES
      if(diff >2):
        diff = (-diff)%NUM_WEDGES

      if(diff <= 2):
        diff_r = abs(regions[a.ring]-regions[ap.ring])
        if(diff_r<=2):
          if(regions[a.ring]>1):
            prob_ap = (0.4/ (2.0**diff_r) * 0.4/(2.0**diff))
          else:
            if(regions[a.ring] == 0):
              prob_ap = (0.4/(2.0**diff))*0.4
              if(diff_r == 2):
                prob_ap *= 0.5
            if(regions[a.ring]==1):
              prob_ap = (0.4/(2.0**diff))
              if(ap.ring == CENTER):
                prob_ap*=0.2
              if(ap.ring == INNER_RING):
                prob_ap*=0.5
              if(ap.ring == FIRST_PATCH):
                prob_ap*=0.2
              if(ap.ring == MIDDLE_RING):
                prob_ap*=0.1
    prob += prob_ap

  return prob


def infiniteValueIteration(gamma):
  # takes a discount factor gamma and convergence cutoff epislon
  # returns

  V = {}
  Q = {}
  V_prime = {}
  
  states = darts.get_states()
  actions = darts.get_actions()

  notConverged = True

  # intialize value of each state to 0
  for s in states:
    V[s] = 0
    Q[s] = {}

  # until convergence is reached
  while notConverged:

    # store values from previous iteration
    for s in states:
      V_prime[s] = V[s]

    # update Q, pi, and V
    for s in states:
      for a in actions:

        # given current state and action, sum product of T and V over all states
        summand = 0
        for s_prime in states:
          summand += T(a, s, s_prime)*V_prime[s_prime]

        # update Q
        Q[s][a] = darts.R(s, a) + gamma*summand

      # given current state, store the action that maximizes V in pi and the corresponding value in V
      PI[s] = actions[0]
      for a in actions:
        if V[s] <= Q[s][a]:
          V[s] = Q[s][a]
          PI[s] = a

    notConverged = False
    for s in states:
      if abs(V[s] - V_prime[s]) > EPSILON:
        notConverged = True
        
  
