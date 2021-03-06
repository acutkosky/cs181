from pickle import load


class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

class DataReader:
  @staticmethod
  def GetImages(filename, limit, target):
    """Returns a list of image objects
            filename: The file to read in
            limit: The maximum number of images to read.  -1 = no limit
            """
    images = []
        
    f = open(filename, 'r')
    data = load(f)
    f.close()
        
    image = None
    for x in data:
        print x
        image = Image(target)
        image.pixels = x
        images.append(image)
        
    return images

  @staticmethod
  def DumpWeights(weights, filename):
    """Dump the weights vector to filename"""
    outfile = open(filename, 'w')
    for weight in weights:
      outfile.write('%r\n' % weight)

  @staticmethod
  def ReadWeights(filename):
    """Returns a weight vector retrieved by reading file filename"""
    infile = open(filename, 'r')
    weights = []
    for line in infile:
      weight = float(line.strip())
      weights.append(weight)
