from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .KindoLogic import Board
import numpy as np

'''
Author: Daniel Scalettar (https://github.com/scalettar/)
Date: March, 2020
'''

class KindoGame(Game):
    '''
    This class specifies the Kindo class
    '''
    
    def __init__(self, n=5):
        self.n = n

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        b = Board(self.n)
        return np.array(b.tiles)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.n, self.n)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        # 5 different placement options, 4 walls or a neutral placement
        # Add 1 action to total; This final index represents no other legal actions
        return self.n * self.n * 5 + 1

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        # Create a copy of the current board
        b = Board(self.n)
        b.tiles = np.copy(board)
        # Get the move being made from the action
        
        
    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        # Array of valid moves to return, initialize to all false (0)
        validMoves = [0] * self.getActionSize()
        # Create a copy of the current board
        b = Board(self.n)
        b.tiles = np.copy(board)
        # Find the legal (valid) moves
        legalMoves = b.get_legal_moves(player)
        # No legal moves found (in Kindo this should only occur when the game is over)
        if len(legalMoves) == 0:
            validMoves[-1] = 1 # last action (move) index means no other moves valid
            return np.array(validMoves)
        for x, y in legalMoves:
            validMoves[self.n * x + y] = 1
        # Convert to np array for performance
        return np.array(validMoves)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        # Create a copy of the current board
        b = board(self.n)
        b.tiles = np.copy(board)
        # Check if player 1 captured player 2's King tile
        if b.tiles[0][4].owner == 1:
            return 1 if player == 1 else -1 
        # Check if player 2 captured player 1's King tile
        if b.tiles[4][0].owner == -1:
            return 1 if player == -1 else -1
        # Check if player 1 has walled in player 2
        if b.tiles[0][2].wallDirection == 2 and b.tiles[1][2].wallDirection == 2 \
            and b.tiles[2][3].wallDirection == 1 and b.tiles[2][4].wallDirection == 1:
            # Check if player 1 owns all the tiles walling in player 2
            if b.tiles[0][2].owner == 1 and b.tiles[1][2].owner == 1 \
            and b.tiles[2][3].owner == 1 and b.tiles[2][4].owner == 1:
                return 1 if player == 1 else -1
        if b.tiles[0][3].wallDirection == 2 and b.tiles[1][4].wallDirection == 1:
            if b.tiles[0][3].owner == 1 and b.tiles[1][4].owner == 1:
                return 1 if player == 1 else -1
        # Check if player 2 has walled in player 1
        if b.tiles[2][0].wallDirection == 3 and b.tiles[2][1].wallDirection == 3 \
            and b.tiles[3][2].wallDirection == 4 and b.tiles[4][2].wallDirection == 4:
            # Check if player 2 owns all the tiles walling in player 1
            if b.tiles[2][0].owner == -1 and b.tiles[2][1].owner == -1 \
            and b.tiles[3][2].owner == -1 and b.tiles[4][2].owner == -1:
                return 1 if player == -1 else 1
        if b.tiles[3][0].wallDirection == 3 and b.tiles[4][1].wallDirection == 4:
            if b.tiles[3][0].owner == -1 and b.tiles[4][1].owner == -1:
                return 1 if player == -1 else -1

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        pass

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass
