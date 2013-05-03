import game_interface
import random
import time
import sys

saw_plant = False
old_life = 0
x = 0
y = 0
logfile = "plant_locs"

def update(view):
  global saw_plant,old_life,x,y,logfile
  plant_bonus = 20
  plant_penalty = 10
  life = view.GetLife()
  if(saw_plant):
    if(life == old_life - plant_penalty-1):
      f = open(logfile,"a")
      f.write(str(x)+" "+str(y)+" P\n")
      f.close()
    else:
      assert(life == old_life-1+plant_bonus)
      f = open(logfile,"a")
      f.write(str(x)+" "+str(y)+" T\n")
      f.close()
    saw_plant = False
  else:
    if(view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT):
      saw_plant = True
      x = view.GetXPos()
      y = view.GetYPos()
      old_life = view.GetLife()

    


def get_move(view):
  # Choose a random direction.
  # If there is a plant in this location, then try and eat it.
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

  xloc = view.GetXPos()
  yloc = view.GetYPos()
  
  if xloc**2+yloc**2<10000:
    move = 0
  else:
    move = random.randint(0,3)
  # Choose a random direction
  #if hasPlant:
  #  for i in xrange(5):
  #    print view.GetImage()
  #time.sleep(0.1)
  return (move, hasPlant)
