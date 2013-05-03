import game_interface
import random
import time

def get_move(view):
#just alternate up, down, left, right, etc.o
    #  round = view.GetRound()%4
    #directions_list = [game_interface.UP, game_interface.LEFT, \
                 #    game_interface.DOWN, game_interface.RIGHT]
                         #choice = directions_list[round]
                         #time.sleep(0.1)
    
#return (choice, False)
  #round = view.GetRound()
                         #if round < 10:
                         #  return (random.randint(0,4), False)
    return (game_interface.DOWN, False)

