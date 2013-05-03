import game_interface
import random
import time
import sys
from pickle import dump,load

saw_plant = False
old_life = 0
good_plants_file = "good_plants"
bad_plants_file = "bad_plants"
plant_image = 0
good_plants = []
bad_plants = []



def update(view):
  global saw_plant,old_life,plant_image,good_plants,bad_plants
  plant_bonus = 20
  plant_penalty = 10
  life = view.GetLife()

#  if(view.GetXPos() == 0 and view.GetYPos() == 0):
#    return

  if(saw_plant):
    if(life == old_life - 1-plant_penalty):
      bad_plants.append(plant_image)
    else:
      print "life: ",life," oldlife: ",old_life
      assert(life == old_life-1+plant_bonus)
      good_plants.append(plant_image)
    saw_plant = False
  else:
    if(view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT):
      saw_plant = True
      plant_image = view.GetImage()
      old_life = view.GetLife()


def add_data(filename,moredata):
  try:
    f = open(filename,"r")
    data =load(f)
    f.close()
  except:
    data = []

  data = data+moredata
  f = open(filename,"w")
  dump(data,f)
  f.close()


def endgame():
  global good_plants,bad_plants,good_plants_file,bad_plants_file

  add_data(good_plants_file,good_plants)
  add_data(bad_plants_file,bad_plants)



def get_move(view):
  # Choose a random direction.
  # If there is a plant in this location, then try and eat it.
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

  xloc = view.GetXPos()
  yloc = view.GetYPos()
  
  #if xloc**2+yloc**2<10000:
  #  move = 0
  #else:
  move = random.randint(0,3)
  # Choose a random direction
  #if hasPlant:
  #  for i in xrange(5):
  #    print view.GetImage()
  #time.sleep(0.1)
  return (move, hasPlant)
