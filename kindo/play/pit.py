import Arena
from MCTS import MCTS
from kindo.KindoGame import KindoGame
from kindo.KindoPlayers import *
from kindo.keras.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

# Play in 4x4 instead of the normal 5x5
mini_kindo = False 
# Play as human against AI agent
human_vs_cpu = True

if mini_kindo:
    g = KindoGame(4)
else:
    g = KindoGame(5)

# Define all players
rp = RandomPlayer(g).play
gp = GreedyKindoPlayer(g).play
hp = HumanKindoPlayer(g).play

# NNet players
n1 = NNet(g)
if mini_kindo:
    n1.load_checkpoint('./pretrained_models/kindo/keras/','[ADD FILE for mini kindo]')
else:
    n1.load_checkpoint('./pretrained_models/kindo/keras/','[ADDFILE for normal kindo]')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    # Player 2 is human
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/kindo/keras/', '[ADDFILE for normal kindo]')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    # Player 2 is AI agent
    player2 = n2p 

# Play game in Arena
arena = Arena.Arena(n1p, player2, g, display=KindoGame.display)

# Display
print(arena.playGames(2, verbose=True))
