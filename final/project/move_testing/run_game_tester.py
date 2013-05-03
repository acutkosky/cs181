import player1.mover
import player2.mover
import game_interface
import random
import signal
import sys
import time
import traceback
from optparse import OptionParser

#to fix the numbering of the directions
print game_interface.UP, game_interface.LEFT, game_interface.DOWN, game_interface.RIGHT

class TimeoutException(Exception):
  def __init__(self):
    pass

def get_move(view, cmd, options, player_id):
  def timeout_handler(signum, frame):
    raise TimeoutException()
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1)
  try: 
    (mv, eat) = cmd(view)
    # Clear the alarm.
    signal.alarm(0)
  except TimeoutException:
    # Return a random value
    # Should probably log this to the interface
    (mv, eat) = (random.randint(0, 4), False)
    error_str = 'Error in move selection (%d).' % view.GetRound()
    if options.display:
      game_interface.curses_debug(player_id, error_str)
    else:
      print error_str
  return (mv, eat)

def print_by_length(s, m):
    for i in range(len(s)):
        print s[i],
        if (i+1)%m == 0:
            print ""


def run_times(options, n):
  num_times_1 = [0,0,0,0]
  num_times_2 = [0,0,0,0]
  for i in range(n):
    (p1, p2) = run(options)
  print "player 1"
#print_by_length(p1, 20)
  print "player 2"
# print_by_length(p2, 20)
  for x in p1:
    num_times_1[x] += 1
  for x in p2:
    num_times_2[x] += 1
  print num_times_1
  print num_times_2
    


def run(options):
  game = game_interface.GameInterface(options.plant_bonus,
                                      options.plant_penalty,
                                      options.observation_cost,
                                      options.starting_life,
                                      options.life_per_turn)
  player1_view = game.GetPlayer1View()
  player2_view = game.GetPlayer2View()

  if options.display:
    if game_interface.curses_init() < 0:
      return
    game_interface.curses_draw_board(game)
  
  # Keep running until one player runs out of life.
  x = 10000
  while x>0:
    (mv1, eat1) = get_move(player1_view, player1.mover.get_move, options, 1)
    (mv2, eat2) = get_move(player2_view, player2.mover.get_move, options, 2)

    game.ExecuteMoves(mv1, eat1, mv2, eat2)
    if options.display:
      game_interface.curses_draw_board(game)
      game_interface.curses_init_round(game)
        #else:
        #print mv1, eat1, mv2, eat2
      #print player1_view.GetLife(), player2_view.GetLife()
    # Check whether someone's life is negative.
      #l1 = player1_view.GetLife()
      #l2 = player2_view.GetLife()
    x -= 1
  return (player1.mover.move_hist, player2.mover.move_hist)

def main(argv):
  parser = OptionParser()
  parser.add_option("-d", action="store", dest="display", default=1, type=int,
                    help="whether to display the GUI board")
  parser.add_option("--plant_bonus", dest="plant_bonus", default=20,
                    help="bonus for eating a nutritious plant",type=int)
  parser.add_option("--plant_penalty", dest="plant_penalty", default=10,
                    help="penalty for eating a poisonous plant",type=int)
  parser.add_option("--observation_cost", dest="observation_cost", default=1,
                    help="cost for getting an image for a plant",type=int)
  parser.add_option("--starting_life", dest="starting_life", default=100,
                    help="starting life",type=int)
  parser.add_option("--life_per_turn", dest="life_per_turn", default=1,
                    help="life spent per turn",type=int)
  (options, args) = parser.parse_args()

  try:
    run_times(options, 1)
  except KeyboardInterrupt:
    if options.display:
      game_interface.curses_close()
  except:
    game_interface.curses_close()
    traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
  main(sys.argv)
