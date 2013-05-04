import plant_pics2 as plant_pics
#import common
def writefile():
  plant_pics.endgame()

def get_move(view):
  plant_pics.update(view)
  return plant_pics.get_move(view)

#def get_move(view):
#  plant_dist.update(view)
#  return plant_dist.get_move(view)

#def get_move(view):
#  return common.get_move(view)

