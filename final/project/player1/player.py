import plant_pics

def writefile():
  plant_pics.endgame()

def get_move(view):
  plant_pics.update(view)
  return plant_pics.get_move(view)
