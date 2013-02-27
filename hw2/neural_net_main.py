from data_reader import *
from neural_net import *
from neural_net_impl import *
from matplotlib import pyplot
import sys
import random


def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'main.py', '-e', 20, '-r', 0.1, '-m', 'Simple' ]) = { '-e':20, '-r':5, '-t': 'simple' }"""
  args_map = {}
  curkey = None
  for i in xrange(1, len(args)):
    if args[i][0] == '-':
      args_map[args[i]] = True
      curkey = args[i]
    else:
      assert curkey
      args_map[curkey] = args[i]
      curkey = None
  return args_map

def validateInput(args):
  args_map = parseArgs(args)
  assert '-e' in args_map, "A number of epochs should be specified with the flag -e (ex: -e 10)"
  assert '-r' in args_map, "A learning rate should be specified with the flag -r (ex: -r 0.1)"
  assert '-t' in args_map, "A network type should be provided. Options are: simple | hidden | custom"
  return(args_map)

def main():

  # Parsing command line arguments
  args_map = validateInput(sys.argv)
  epochs = int(args_map['-e'])
  rate = float(args_map['-r'])
  networkType = args_map['-t']
  show_plot = '-d' in args_map
  if('-s' in args_map):
    savename = args_map['-s']
  else:
    savename = False
  # Load in the training data.
  images = DataReader.GetImages('training-9k.txt', -1)
  for image in images:
    assert len(image.pixels) == 14
    assert len(image.pixels[0]) == 14

  # Load the validation set.
  validation = DataReader.GetImages('validation-1k.txt', -1)
  for image in validation:
    assert len(image.pixels) == 14
    assert len(image.pixels[0]) == 14

  # Initializing network

  if networkType == 'simple':
    network = SimpleNetwork()
  if networkType == 'hidden':
    network = HiddenNetwork()
  if networkType == 'custom':
    network = CustomNetwork()

  # Hooks user-implemented functions to network
  network.FeedForwardFn = FeedForward
  network.TrainFn = Train

  # Initialize network weights
  network.InitializeWeights()
  

  # Displays information
  print '* * * * * * * * *'
  print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
  print 'Type of network used: %s' % network.__class__.__name__
  print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
         (len(network.network.inputs), len(network.network.hidden_nodes),
          len(network.network.outputs)))
  if(show_plot):
    if(savename != False):
      print 'Will display plot, saving to %s' % (savename)
    else:
      print 'Will display plot without saving'
  else:
    if(savename!=False):
      print 'Will save plot to %s without displaying' %(savename)
  print '* * * * * * * * *'
  # Train the network.
  log = network.Train(images, validation, rate, epochs)
  epochs = range(0,epochs+1)
  trainingerrors = [1.0-x[0] for x in log]
  validationerrors = [1.0-x[1] for x in log]
  
  pyplot.plot(epochs,trainingerrors,label="training error")
  pyplot.plot(epochs,validationerrors,label="validation error")
  pyplot.title("Training and Validation Error for "+networkType+" network")
  pyplot.legend()
  if(savename != False):
    pyplot.savefig(savename)
  if(show_plot):
    pyplot.show()


if __name__ == "__main__":
  main()
