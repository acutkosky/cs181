from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input
import random


# <--- Problem 3, Question 1 --->

def FeedForward(network, input):
  """
  Arguments:
  ---------
  network : a NeuralNetwork instance
  input   : an Input instance

  Returns:
  --------
  Nothing

   Description:
  -----------
  This function propagates the inputs through the network. That is,
  it modifies the *raw_value* and *transformed_value* attributes of the
  nodes in the network, starting from the input nodes.

  Notes:
  -----
  The *input* arguments is an instance of Input, and contains just one
  attribute, *values*, which is a list of pixel values. The list is the
  same length as the number of input nodes in the network.

  i.e: len(input.values) == len(network.inputs)

  This is a distributed input encoding (see lecture notes 7 for more
  informations on encoding)

  In particular, you should initialize the input nodes using these input
  values:

  network.inputs[i].raw_value = input[i]
  """
  network.CheckComplete()

  assert len(input.values) == len(network.inputs)

  # 1) Assign input values to input nodes
  for i in range(len(input.values)):
    network.inputs[i].raw_value = input.values[i]
    network.inputs[i].transformed_value = input.values[i]


  # 2) Propagates to hidden layer
  for node in network.hidden_nodes:
    node.raw_value=NeuralNetwork.ComputeRawValue(node)
    node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value)

  # 3) Propagates to the output layer
  for node in network.outputs:
    node.raw_value=NeuralNetwork.ComputeRawValue(node)
    node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value)


#< --- Problem 3, Question 2

def Backprop(network, input, target, learning_rate):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  input         : an Input instance
  target        : a target instance
  learning_rate : the learning rate (a float)

  Returns:
  -------
  Nothing

  Description:
  -----------
  The function first propagates the inputs through the network
  using the Feedforward function, then backtracks and update the
  weights.

  Notes:
  ------
  The remarks made for *FeedForward* hold here too.

  The *target* argument is an instance of the class *Target* and
  has one attribute, *values*, which has the same length as the
  number of output nodes in the network.

  i.e: len(target.values) == len(network.outputs)

  In the distributed output encoding scenario, the target.values
  list has 10 elements.

  When computing the error of the output node, you should consider
  that for each output node, the target (that is, the true output)
  is target[i], and the predicted output is network.outputs[i].transformed_value.
  In particular, the error should be a function of:

  target[i] - network.outputs[i].transformed_value
  
  """
  network.CheckComplete()
  # 1) We first propagate the input through the network
  FeedForward(network,input)
  # 2) Then we compute the errors and update the weigths starting with the last layer
  
  #first the outputs, which have no children (let's practice going in backwards order here):
  for i in range(len(network.outputs))[::-1]:
    er = target[i] - network.outputs[i].transformed_value
    network.outputs[i].delta = NeuralNetwork.SigmoidPrime(network.outputs[i].raw_value)*er
    
  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  for i in range(len(network.hidden_nodes))[::-1]:
    er = 0
    for j in range(len(network.hidden_nodes[i].forward_weights)):
      er += network.hidden_nodes[i].forward_weights[j].value*network.hidden_nodes[i].forward_neighbors[j].delta
    network.hidden_nodes[i].delta = NeuralNetwork.SigmoidPrime(network.hidden_nodes[i].raw_value)*er

  for i in range(len(network.inputs))[::-1]:
    er = 0
    for j in range(len(network.inputs[i].forward_weights)):
      er += network.inputs[i].forward_weights[j].value*network.inputs[i].forward_neighbors[j].delta
    network.inputs[i].delta = NeuralNetwork.SigmoidPrime(network.inputs[i].raw_value)*er




  for node in network.outputs:
    for i in range(len(node.inputs)):
      node.weights[i].value  += learning_rate*node.inputs[i].transformed_value*node.delta


  for node in network.hidden_nodes:
    for i in range(len(node.inputs)):
      node.weights[i].value  += learning_rate*node.inputs[i].transformed_value*node.delta




# <--- Problem 3, Question 3 --->

def Train(network, inputs, targets, learning_rate, epochs):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  inputs        : a list of Input instances
  targets       : a list of Target instances
  learning_rate : a learning_rate (a float)
  epochs        : a number of epochs (an integer)

  Returns:
  -------
  Nothing

  Description:
  -----------
  This function should train the network for a given number of epochs. That is,
  run the *Backprop* over the training set *epochs*-times
  """

  network.CheckComplete()


  for i in range(epochs):
    for i in range(len(inputs)):
      Backprop(network,inputs[i],targets[i],learning_rate)

  


# <--- Problem 3, Question 4 --->

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    """
    Initializatio.
    YOU DO NOT NEED TO MODIFY THIS __init__ method
    """
    super(EncodedNetworkFramework, self).__init__() # < Don't remove this line >
    
  # <--- Fill in the methods below --->

  def EncodeLabel(self, label):
    """
    Arguments:
    ---------
    label: a number between 0 and 9

    Returns:
    ---------
    a list of length 10 representing the distributed
    encoding of the output.

    Description:
    -----------
    Computes the distributed encoding of a given label.

    Example:
    -------
    0 => [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    3 => [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    Notes:
    ----
    Make sure that the elements of the encoding are floats.
    
    """
    # Replace line below by content of function
    ret = [0.0]*10
    ret[label] = 1.0
    return ret

  def GetNetworkLabel(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    the 'best matching' label corresponding to the current output encoding

    Description:
    -----------
    The function looks for the transformed_value of each output, then decides 
    which label to attribute to this list of outputs. The idea is to 'line up'
    the outputs, and consider that the label is the index of the output with the
    highest *transformed_value* attribute

    Example:
    -------

    # Imagine that we have:
    map(lambda node: node.transformed_value, self.network.outputs) => [0.2, 0.1, 0.01, 0.7, 0.23, 0.31, 0, 0, 0, 0.1, 0]

    # Then the returned value (i.e, the label) should be the index of the item 0.7,
    # which is 3
    
    """
    # Replace line below by content of function

    outputs = map(lambda node: node.transformed_value, self.network.outputs)

    ret = 0 
    maxval = 0
    for i in range(len(outputs)):
      if outputs[i]>maxval:
        ret = i
        maxval = outputs[i]
    return ret




  def Convert(self, image):
    """
    Arguments:
    ---------
    image: an Image instance

    Returns:
    -------
    an instance of Input

    Description:
    -----------
    The *image* arguments has 2 attributes: *label* which indicates
    the digit represented by the image, and *pixels* a matrix 14 x 14
    represented by a list (first list is the first row, second list the
    second row, ... ), containing numbers whose values are comprised
    between 0 and 256.0. The function transforms this into a unique list
    of 14 x 14 items, with normalized values (that is, the maximum possible
    value should be 1).
    
    """
    # Replace line below by content of function

    values = []
      #    comp = [pixel/256.0 for pixel in sublist in image.pixels]
    for row in image.pixels:
      values += map(lambda x:x/256.0,row)
    ret = Input()
    ret.values = values
    return ret


  def InitializeWeights(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes the weights with random values between [-0.01, 0.01].

    Hint:
    -----
    Consider the *random* module. You may use the the *weights* attribute
    of self.network.
    
    """
    # replace line below by content of function

    for weight in self.network.weights:
      weight.value = (0.1/0.5)*(random.random()-0.5)
    




#<--- Problem 3, Question 6 --->

class SimpleNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a simple network, with 196 input nodes,
    10 output nodes, and NO hidden nodes. Each input node
    should be connected to every output node.
    """
    super(SimpleNetwork, self).__init__() # < Don't remove this line >
    
    # 1) Adds an input node for each pixel.    

    for i in range(196):
      self.network.AddNode(Node(),NeuralNetwork.INPUT)


    # 2) Add an output node for each possible digit label.
    for i in range(10):
      anode = Node()
      for node in self.network.inputs:
        anode.AddInput(node,0,self.network)
      self.network.AddNode(anode,NeuralNetwork.OUTPUT)

    self.InitializeWeights()





#<---- Problem 3, Question 7 --->

class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=15):
    """
    Arguments:
    ---------
    number_of_hidden_nodes : the number of hidden nodes to create (an integer)

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a network with a hidden layer. The network
    should have 196 input nodes, the specified number of
    hidden nodes, and 10 output nodes. The network should be,
    again, fully connected. That is, each input node is connected
    to every hidden node, and each hidden_node is connected to
    every output node.
    """
    super(HiddenNetwork, self).__init__() # < Don't remove this line >

    # 1) Adds an input node for each pixel


    for i in range(196):
      self.network.AddNode(Node(),NeuralNetwork.INPUT)

    
    # 2) Adds the hidden layer
    for i in range(number_of_hidden_nodes):
      anode = Node()
      for node in self.network.inputs:
        anode.AddInput(node,0,self.network)
      self.network.AddNode(anode,NeuralNetwork.HIDDEN)


    # 3) Add an output node for each possible digit label.
    for i in range(10):
      anode = Node()
      for node in self.network.hidden_nodes:
        anode.AddInput(node,0,self.network)
      self.network.AddNode(anode,NeuralNetwork.OUTPUT)

    self.InitializeWeights()



#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self, number_layer2 = 30):
    """
    Arguments:
    ---------
    number_layer1 - the number of hidden nodes in the first layer
    number_layer2 - the number of hidden nodes in the second hidden lyaer

    Returns:
    --------

    none

    Description:
    -----------
    Makes a network with two hidden layers.
    """
    super(CustomNetwork, self).__init__() # <Don't remove this line>

    # 1) Adds an input node for each pixel


    for i in range(196):
      self.network.AddNode(Node(),NeuralNetwork.INPUT)

    
    # 2) Adds the hidden layer
      # this layer is FORCED to be local, i.e. depend only one localized groups
      # of nodes 
    hidlayer1 = []
    for i in range(1, 14,3):
        for j in range(1, 14,3):
            anode = Node()
            inputs = self.network.inputs
            for row in range(i-1, i+1):
                for column in range(j-1, j+1):
                    anode.AddInput(inputs[14*(row)+(column)], 0, self.network)
                #                       for node in self.network.inputs:
                        #anode.AddInput(node,0,self.network)
            self.network.AddNode(anode,NeuralNetwork.HIDDEN)
            hidlayer1.append(anode)

        
    # 3) Adds Another hidden layer
    hidlayer2 = []
    for i in range(number_layer2):
      anode = Node()
      for node in hidlayer1:
        anode.AddInput(node,0,self.network)
      self.network.AddNode(anode,NeuralNetwork.HIDDEN)
      hidlayer2.append(anode)


    # 4) Add an output node for each possible digit label.
    for i in range(10):
      anode = Node()
      for node in hidlayer2:
        anode.AddInput(node,0,self.network)
      self.network.AddNode(anode,NeuralNetwork.OUTPUT)

    self.InitializeWeights()

    pass
