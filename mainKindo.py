from Coach import Coach
from kindo.KindoGame import KindoGame as Game
from kindo.pytorch.NNet import NNetWrapper as nn
from utils import *

args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/5x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

if __name__ == "__main__":
    # Create game object passing in board dimension
    g = Game(5)
    # Create neural network passing in the game object
    nnet = nn(g)

    # Load from checkpoint if flag set
    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    # Create coach object which executes self-play and learning
    # using the functions defined in KindoGame and Kindo's NeuralNet
    c = Coach(g, nnet, args)
    # Load training examples if flag set
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    # Learn using coach
    c.learn()
