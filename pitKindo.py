import Arena
from MCTS import MCTS
from kindo.KindoGame import KindoGame
from kindo.KindoPlayers import *
from kindo.pytorch.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
# Play in 4x4 instead of the normal 5x5
mini_kindo = False 
# Player types:
# 0: human, 1: nn, 2: greedy, else: random
player1_type = 0
player2_type = 3

if mini_kindo:
    g = KindoGame(4)
else:
    g = KindoGame(5)

# Define all players (these are actually setting the 'play' functions that will be used)
# See Arena.py for description on how this works
hp = HumanKindoPlayer(g).play
gp = GreedyKindoPlayer(g).play
rp = RandomPlayer(g).play

# NNet player 1
# n1 = NNet(g)
# if mini_kindo:
#     n1.load_checkpoint('./pretrained_models/kindo/pytorch/','4x100x25_best.pth.tar')
# else:
#     n1.load_checkpoint('./pretrained_models/kindo/pytorch/','5x100x25_best.pth.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(g, n1, args1)
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

# # NNet player 2
# n2 = NNet(g)
# if mini_kindo:
#     n2.load_checkpoint('./pretrained_models/kindo/pytorch/','4x100x25_best.pth.tar')
# else:
#     n2.load_checkpoint('./pretrained_models/kindo/pytorch/','5x100x25_best.pth.tar')
# args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
# mcts2 = MCTS(g, n2, args2)
# n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

# Set player 1
if player1_type == 0:
    player1 = hp
# elif player1_type == 1:
    # player1 = n1p
elif player1_type == 2:
    player1 = gp
else:
    player1 = rp
# Set player 2
if player2_type == 0:
    player2 = hp
# elif player2_type == 1:
    # player2 = n2p
elif player2_type == 2:
    player2 = gp
else:
    player2 = rp


# Play game in Arena
arena = Arena.Arena(player1, player2, g, display=KindoGame.display)

# Display
print(arena.playGames(2, verbose=True))
