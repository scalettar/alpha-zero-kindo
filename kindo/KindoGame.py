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
    This class specifies the Kindo game.
    It interacts with the Board class which controls the game state.
    '''

    # For displaying board in text format
    display_owner = {
        1: "x",
        0: " ",
        -1: "o"
    }
    display_wallDirection = {
        1: ".",
        2: ":",
        3: ".",
        4: ":" 
    }
    display_hasDot = {
        True: "-",
        False: " "
    }
    display_isKing = {
        True: "K",
        False: " "
    }
    display_isUnwallable = {
        True: ".",
        False: " "
    }
    
    def __init__(self, n=5):
        # Board dimensions n x n
        self.n = n
        # Number of different types of tiles a player can have
        # 0: No wall
        # 1: Wall facing up
        # 2: Wall facing right
        # 3: Wall facing down
        # 4: Wall facing left
        self.tileTypes = 5

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
        # 5 different tile placement options, 4 walls or a neutral placement
        # Add 1 action to total; This final index represents no other legal actions

        # e.g. for n = 5 (5 x 5 board):
        # STARTING INDICES FOR TILE PLACEMENT ACTIONS FOR EACH TILE (5 actions per tile)
        # 		0	1	2	3	4
        # 	-----------------------
        # 0	|	0	5	10	15	20
        # 1	|	25	30	35	40	45
        # 2	|	50	55	60	65	70
        # 3	|	75	80	85	90	95
        # 4	|	100	105	110	115	120
        # Actions 0 - 124 represent a move of form (x, y, w) flattened into a single index
        # Action 125 is only true if actions 0 - 124 are all invalid
        
        # EXAMPLE 1. 
        # A move (x, y, w) = (3, 2, 4) would mean placing a left facing wall 
        # in space with x-coordinate = 3 and y-coordinate = 2
        # This move cooresponds with action 85 + 4 = 89

        # EXAMPLE 2.
        # Action 90 would coorespond with move (3, 3, 0)
        # This means capturing tile with x-coordinate = 3 and y-coordinate = 3
        # without placing any walls
        return self.n * self.n * self.tileTypes + 1

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
        # Check if no valid actions
        if action == self.getActionSize() - 1:
            # No valid actions, in Kindo this means the game must be over so make no changes
            return (board, player)
        # Create a copy of the current board
        b = Board(self.n)
        b.tiles = np.copy(board)
        # Get move (x, y, w) from flattened action index
        x = int(action / (self.n * self.tileTypes))
        y = int((action % (self.n * self.tileTypes)) / self.tileTypes)
        w = (action % (self.n * self.tileTypes)) % self.tileTypes
        move = (x, y, w)
        # Execute move
        currentPlayerID = b.execute_move(move, player)
        # Return updated state and current player
        return (b.tiles, currentPlayerID)
        
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
            validMoves[-1] = 1 # last move (action) index means no other moves are valid
            return np.array(validMoves)
        # Create flattened array of valid moves (actions) from legalMoves list
        for x, y, w in legalMoves:
            validMoves[(x * self.n * self.tileTypes) + (y * self.tileTypes) + w] = 1
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
        b = Board(self.n)
        b.tiles = np.copy(board)
        # Check if any of the terminal conditions have been reached
        kingCaptured = b.king_captured(player)
        walledIn = b.walled_in(player)
        if kingCaptured == 1 or walledIn == 1:
            # A win condition was satisfied by the player
            return 1
        if kingCaptured == -1 or walledIn == -1:
            # A win condition was satisfied by the opponent
            return -1
        else:
            # Neither player satisfied a win condition
            return 0

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
        # Create a copy of the current board
        b = Board(self.n)
        b.tiles = np.copy(board)
        # If player 2 swap owner of all tiles on board
        if player == -1:
            b.swap_all_tile_owners()
        # return canonical board
        return np.array(b.tiles)

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
        # Check for correct pi length
        assert(len(pi) == self.getActionSize())
        pi_board = np.reshape(pi[:-1], (self.n, self.n, self.tileTypes))
        symmetries_list = []
        # Generate symmetries
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                symmetries_list += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return symmetries_list


    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        board.tostring()

    def getScore(self, board, player):
        '''
        Simple evaluation function used by GreedyKindoPlayer to choose action
        '''
        b = Board(self.n)
        b.tiles = np.copy(board)
        return b.get_tilesOwned_dif(player)

    @staticmethod
    def display(board):
        '''
        Displays board (see Kindo README.md for explanation)
        '''
        #       0       1       2       3       4    
        #   -----------------------------------------
        #   |       |       |       |       |       |
        # 0 |       |       |       |       |       |
        #   |       |       |       |       |       |
        #   -----------------------------------------
        #   |       |       |       |       |       |
        # 1 |       |       |       |       |       |
        #   |       |       |       |       |       |
        #   -----------------------------------------
        #   |       |       |       |       |       |
        # 2 |       |       |       |       |       |
        #   |       |       |       |       |       |
        #   -----------------------------------------
        #   |       |       |       |       |       |
        # 3 |       |       |       |       |       |
        #   |       |       |       |       |       |
        #   -----------------------------------------
        #   |       |       |       |       |       |
        # 4 |       |       |       |       |       |
        #   |       |       |       |       |       |
        #   ----------------------------------------- 
        n = board.shape[0]
        b = Board(n)
        b.tiles = np.copy(board)
        # Print number of moves for each player
        # Player 1 Moves: current turn | next turn
        # Player 2 Moves: current turn | next turn
        print("Player 1 Moves:", b.tiles[n-1, 0, 6], "|", b.tiles[n-1, 0, 7])
        print("Player -1 Moves:", b.tiles[0, n-1, 6], "|", b.tiles[0, n-1, 7])
        print("____________________________________________")
        print("")
        # Print y-coordinate key
        print("       ", end="")
        for y in range(n):
            print(y, end="       ")
        # Print top board border
        print("")
        print("   -----------------------------------------")
        # Iterate over rows x
        for x in range(n):
            owner = []
            wallDirection = []
            hasDot = []
            isKing = []
            isUnwallable = []
            # Get tile values
            for y in range(n):
                owner.append(board[x, y, 0])
                wallDirection.append(board[x, y, 1])
                hasDot.append(board[x, y, 2])
                isKing.append(board[x, y, 3])
                isUnwallable.append(board[x, y, 4])
            # Print top line of row x
            print("   |", end="")
            for y in range(n):
                # Get tile values at index y
                o = owner[y]
                wD = wallDirection[y]
                hD = hasDot[y]
                iK = isKing[y]
                iU = isUnwallable[y]
                # First
                print(" ", end="")
                # Second (top left)
                if iU:
                    print(KindoGame.display_isUnwallable[iU], end="")
                elif wD == 1 or wD == 4:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Third
                if wD == 1:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Fourth (top middle)
                if iK == True:
                    print(KindoGame.display_isKing[iK], end="")
                elif wD == 1:
                    print(KindoGame.display_wallDirection[wD], end="")
                elif hD == True:
                    print(KindoGame.display_hasDot[hD], end="")
                else:
                    print(" ", end="")
                # Fifth
                if wD == 1:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Sixth (top right)
                if isUnwallable[y]:
                    print(KindoGame.display_isUnwallable[iU], end="")
                elif wD == 1 or wD == 2:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Seventh
                print(" |", end="")
            print("")
            # Print middle line of row x
            print("", x, "|", end="")
            for y in range(n):
                # Get tile values at index y
                o = owner[y]
                wD = wallDirection[y]
                hD = hasDot[y]
                iK = isKing[y]
                iU = isUnwallable[y]
                # First
                print(" ", end="")
                # Second (middle left)
                if iK == True:
                    print(KindoGame.display_isKing[iK], end="")
                elif wD == 4:
                    print(KindoGame.display_wallDirection[wD], end="")
                elif hD == True:
                    print(KindoGame.display_hasDot[hD], end="")
                else:
                    print(" ", end="")
                # Third
                print(" ", end="")
                # Fourth (middle middle i.e. center)
                print(KindoGame.display_owner[o], end="")
                # Fifth
                print(" ", end="")
                # Sixth (middle right)
                if iK == True:
                    print(KindoGame.display_isKing[iK], end="")
                elif wD == 2:
                    print(KindoGame.display_wallDirection[wD], end="")
                elif hD == True:
                    print(KindoGame.display_hasDot[hD], end="")
                else:
                    print(" ", end="")
                # Seventh
                print(" |", end="")
            print("")
            # Print bottom line of row x
            print("   |", end="")
            for y in range(n):
                # Get tile values at index y
                o = owner[y]
                wD = wallDirection[y]
                hD = hasDot[y]
                iK = isKing[y]
                iU = isUnwallable[y]
                # First
                print(" ", end="")
                # Second (bottom left)
                if iU == True:
                    print(KindoGame.display_isUnwallable[iU], end="")
                elif wD == 3 or wD == 4:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Third
                if wD == 3:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Fourth (bottom middle)
                if iK == True:
                    print(KindoGame.display_isKing[iK], end="")
                elif wD == 3:
                    print(KindoGame.display_wallDirection[wD], end="")
                elif hD == True:
                    print(KindoGame.display_hasDot[hD], end="")
                else:
                    print(" ", end="")
                # Fifth
                if wD == 3:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Sixth (bottom right)
                if iU == True:
                    print(KindoGame.display_isUnwallable[iU], end="")
                elif wD == 2 or wD == 3:
                    print(KindoGame.display_wallDirection[wD], end="")
                else:
                    print(" ", end="")
                # Seventh
                print(" |", end="")
            print("")
            # Print bottom boarder of row tiles
            print("   -----------------------------------------")