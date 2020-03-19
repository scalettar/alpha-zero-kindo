import math

'''
Author: Daniel Scalettar (https://github.com/scalettar/)
Date: March, 2020
'''
    
class Board():
    '''
    This class specifies the board for Kindo.
    The board effectively represents the state of the game.

    Board properties:
        board[x][y], x indexes columns, y indexes rows, (0, 0) is top left
        values: 1 = player 1, -1 = player 2, 0 = neutral
    '''
    def __init__(self, n):
        """
        Initializes starting board state
        """
        # Define constant parameters
        self.MOVES_MAX = 4 # maximum current or next turn moves a player can have
        self.MOVES_NEXT_BASE = 2 # base moves for start of turn without bonus moves
        # Define constant initial parameters
        self.INIT_P1_MOVES = 1 # initial number of moves for p1
        self.INIT_P2_MOVES = 0 # initial number of moves for p2
        self.INIT_P1_MOVES_NEXT = 2 # initial number of moves for p1's next turn
        self.INIT_P2_MOVES_NEXT = 2 # initial number of moves for p2's next turn
        # Set board dimensions (n x n)
        self.n = n
        # Create the board array of Tile objects
        self.tiles = [[Tile(0, 0, False, False, False, 0, 0, 0, 0) for i in range(self.n)] \
            for j in range(self.n)]
        # Set King tiles
        self.tiles[self.n-1][0].owner = 1
        self.tiles[self.n-1][0].isKing = True
        self.tiles[self.n-1][0].isUnwallable = True
        self.tiles[0][self.n-1].owner = -1
        self.tiles[0][self.n-1].isKing = True
        self.tiles[0][self.n-1].isUnwallable = True
        # Set unwallable tiles (cannot place walls on these tiles)
        for i in range(self.n):
            self.tiles[i][i].isUnwallable = True
        # Set Player values
        self.tiles[self.n-1][0].playerID = 1
        self.tiles[self.n-1][0].movesCurrent = self.INIT_P1_MOVES
        self.tiles[self.n-1][0].movesNext = self.INIT_P1_MOVES_NEXT
        self.tiles[self.n-1][0].numTilesOwned = 1
        self.tiles[0][self.n-1].playerID = -1
        self.tiles[0][self.n-1].movesCurrent = self.INIT_P2_MOVES
        self.tiles[0][self.n-1].movesNext = self.INIT_P2_MOVES_NEXT
        self.tiles[0][self.n-1].numTilesOwned = 1
        # Create Player objects (Unused, player info will be stored in Tile object instead)
        # self.player1 = Player(1, self.INIT_P1_MOVES, self.INIT_P1_MOVES_NEXT, 1)
        # self.player2 = Player(-1, self.INIT_P2_MOVES, self.INIT_P2_MOVES_NEXT, 1)
        # Create the current and opposing player reference objects
        # this_player = self.player1
        # self.opposingPlayer = self.player2

    def get_legal_moves(self, player):
        '''
        Returns all the legal moves for the player in the given board state
        Actions 
        '''
        # Create set to store legal moves
        legalMoves = set()
        # Check each tile
        for x in range(self.n):
            for y in range(self.n):
                # Check tile owner
                if self.tiles[x][y].owner == player and not (self.tiles[x][y].isUnwallable):
                    # Tile already owned by current player
                    # Valid moves: placing any wall not already on the tile in same direction
                    newMoves = []
                    for i in range(1, 5):
                        if i != self.tiles[x][y].wallDirection:
                            # No wall already facing that direction on tile x, y
                            newMoves.append((x, y, i))
                    legalMoves.update(newMoves)
                else:
                    # Tile not owned by current player
                    # Valid moves: capture tile if an adjacent tile owned by player
                    # and is not being blocked by a wall on this tile
                    newMoves = []
                    if self._check_valid_adjacent(x, y, player):
                        newMoves.append((x, y, 0))
                    legalMoves.update(newMoves)
        return list(legalMoves)

    def execute_move(self, move, player):
        '''
        Executes given move where move is in the format (x, y, w)
        x: x-coordinate of targeted tile
        y: y-coordinate of targeted tile
        w: type of tile to place (wallDirection of Tile)
        '''
        # Get appropriate player info given player
        currentPlayer = self._get_this_player(player)
        opposingPlayer = self._get_other_player(player)
        # Extract move parameters x, y, and w
        (x, y, w) = move
        # Execute move depending on type (capturing or placing wall)
        if w != 0: # Placing Wall Action
            # Update direction of wall on tile
            self.tiles[x][y].wallDirection = w
            # Subtract a move from the current player
            currentPlayer.movesCurrent -= 1
        else: # Capturing Action
            if self.tiles[x][y].owner == 0: # Tile at x, y is neutral
                # Current player captures tile
                self.tiles[x][y].owner = currentPlayer.playerID
                self.tiles[x][y].hasDot = True
                currentPlayer.movesCurrent -= 1
                currentPlayer.numTilesOwned += 1
            else: # Tile at x, y is owned by opposing player
                # Check if tile has a dot and award opponent a bonus move if true
                if self.tiles[x][y].hasDot == True \
                    and opposingPlayer.movesNext < self.MOVES_MAX:
                    opposingPlayer.movesNext += 1
                # Current player captures tile
                self.tiles[x][y].owner = currentPlayer.playerID
                self.tiles[x][y].hasDot = True
                self.tiles[x][y].wallDirection = 0
                currentPlayer.movesCurrent -= 1
                currentPlayer.numTilesOwned += 1
                opposingPlayer.numTilesOwned -= 1
                # Check if any other tiles were detached from opponent's King tile
                connectedOpponent = self._get_connected_tiles(opposingPlayer.playerID)
                connectedTilesNum = len(connectedOpponent)
                if connectedTilesNum < opposingPlayer.numTilesOwned:
                    # Mass capture detached tiles (swap from opponent to current player)
                    self._mass_capture(currentPlayer, opposingPlayer, connectedOpponent)
                    # Award bonus move to current player for detaching opponent tiles
                    if currentPlayer.movesNext < self.MOVES_MAX:
                        currentPlayer.movesNext += 1
                    # Update number of tiles owned for both players
                    numMassCaptured = opposingPlayer.numTilesOwned - connectedTilesNum
                    currentPlayer.numTilesOwned += numMassCaptured
                    opposingPlayer.numTilesOwned -= numMassCaptured 
        # Determine which player is making the next move
        if currentPlayer.movesCurrent < 1:
            temp = currentPlayer
            currentPlayer = opposingPlayer
            opposingPlayer = temp
            # New current player's moves are updated to be equal to that player's next moves
            currentPlayer.moves = currentPlayer.movesNext
            # New current player's next moves are set to default base number of next moves
            currentPlayer.movesNext = self.MOVES_NEXT_BASE
            # Remove dots from new current player's tiles
            self._new_turn_clear_dots(currentPlayer)
        # Update player
        if currentPlayer.playerID == 1:
            self.tiles[self.n-1][0] = currentPlayer
            self.tiles[0][self.n-1] = opposingPlayer
        else:
            self.tiles[self.n-1][0] = opposingPlayer
            self.tiles[0][self.n-1] = currentPlayer
        return currentPlayer.playerID

    def _check_valid_adjacent(self, x, y, player):
        '''
        Checks if there is a horizontally or vertically adjacent tile to x, y which is:
        1. owned by the current player (player)
        2. not blocked by a wall on x, y
        '''
        if self.tiles[x][y].wallDirection != 1:
            # No wall facing up, check if player owns tile above
            if x != 0 and self.tiles[x-1][y].owner == player:
                return True
        if self.tiles[x][y].wallDirection != 2:
            # No wall facing right, check if player owns tile to right
            if y != self.n-1 and self.tiles[x][y+1].owner == player:
                return True
        if self.tiles[x][y].wallDirection != 3:
            # No wall facing down, check if player owns tile below
            if x != self.n-1 and self.tiles[x+1][y].owner == player:
                return True
        if self.tiles[x][y].wallDirection != 4:
            # No wall facing left, check if player owns tile to left
            if y != 0 and self.tiles[x][y-1].owner == player:
                return True
        # No valid adjacent player owned tiles to tile at x, y
        return False

    def _get_connected_tiles(self, player):
        '''
        Finds and returns a list of all tiles connected to player's King tile
        The list uses a flattened index converted from (x, y) coordinate pairs
        e.g. for n = 5 (5 x 5 board):
                0	1	2	3	4
        	-----------------------
        0	|	0	1	2	3	4
        1	|	5	6	7	8	9
        2	|	10	11	12	13	14
        3	|	15	16	17	18	19
        4	|	20	21	22	23	24
        '''
        # List of connected tiles
        connected = []
        # Stack to traverse through tiles connected to player's King tile
        stack = []
        # Push the corresponding player's King tile onto the stack
        if player == self.tiles[self.n-1][0].playerID:
            stack.append(self.n * (self.n - 1))
        else:
            stack.append(self.n - 1)
        # Find connected tiles using stack
        while len(stack):
            # Explore tile corresponding to first flattened index in stack
            currentIndex = stack.pop()
            # Get x and y from flattened index
            x = math.floor(currentIndex / self.n)
            y = currentIndex % self.n
            # If tile is not already in connected array, check if connected
            if not currentIndex in connected:
                # Check if tile belongs to player
                if self.tiles[x][y].owner == player:
                    # Tile belongs to player so add to connected
                    connected.append(currentIndex)
                    # Check if adjacent tiles are also connected
                    if currentIndex > (self.n - 1): # Check tile above
                        stack.append(currentIndex - self.n)
                    if (currentIndex + 1) % self.n != 0: # Check tile to right
                        stack.append(currentIndex + 1)
                    if currentIndex < (self.n * (self.n + 1)): # Check tile below
                        stack.append(currentIndex + self.n)
                    if currentIndex % self.n != 0: # Check tile to left
                        stack.append(currentIndex - 1)
        return connected

    def _mass_capture(self, currentPlayer, opposingPlayer, connectedOpponent):
        '''
        Swaps ownership from opponent to player of all tiles owned by opponent but
        no longer connected
        '''
        # Check each tile on board and see if ownership swap is needed
        for x in range(self.n):
            for y in range(self.n):
                # Check if tile owned by opponent is no longer connected
                if self.tiles[x][y].owner == opposingPlayer.playerID \
                    and not (connectedOpponent[x][y] == opposingPlayer.playerID):
                    # Swap tile owner from opponent to current player
                    self.tiles[x][y].owner = currentPlayer
                    # Remove any walls and dots from the tile
                    self.tiles[x][y].hasDot = False
                    self.tiles[x][y].wallDirection = 0

    def _new_turn_clear_dots(self, this_player):
        '''
        Clear dots from new current player's tiles
        '''
        for x in range(self.n):
            for y in range(self.n):
                if self.tiles[x][y].owner == this_player.playerID:
                    self.tiles[x][y].hasDot = False
        
    def king_captured(self, player):
        '''
        Checks if a King tile has been captured
        If yes, returns winning player (1 or -1)
        Else returns 0
        '''
        # Check if player 1 captured player 2's King tile
        if self.tiles[0][self.n-1].owner == 1:
            return 1 if player == 1 else -1
        # Check if player 2 captured player 1's King tile
        if self.tiles[self.n-1][0].owner == -1:
            return 1 if player == -1 else -1
        # No King tile has been captured
        return 0

    def walled_in(self, player):
        '''
        !!!WARNING!!! This method only works for n=5, needs to be generalized
        Checks if a player has been walled in (impossible to ever capture enemy King)
        If yes, returns winning player (1 or -1)
        Else returns 0
        '''
        # Check if player 1 has walled in player 2
        if self.tiles[0][2].wallDirection == 2 and self.tiles[1][2].wallDirection == 2 \
            and self.tiles[2][3].wallDirection == 1 and self.tiles[2][4].wallDirection == 1:
            # Check if player 1 owns all the tiles walling in player 2
            if self.tiles[0][2].owner == 1 and self.tiles[1][2].owner == 1 \
            and self.tiles[2][3].owner == 1 and self.tiles[2][4].owner == 1:
                return 1 if player == 1 else -1
        if self.tiles[0][3].wallDirection == 2 and self.tiles[1][4].wallDirection == 1:
            # Check if player 1 owns all the tiles walling in player 2
            if self.tiles[0][3].owner == 1 and self.tiles[1][4].owner == 1:
                return 1 if player == 1 else -1
        # Check if player 2 has walled in player 1
        if self.tiles[2][0].wallDirection == 3 and self.tiles[2][1].wallDirection == 3 \
            and self.tiles[3][2].wallDirection == 4 and self.tiles[4][2].wallDirection == 4:
            # Check if player 2 owns all the tiles walling in player 1
            if self.tiles[2][0].owner == -1 and self.tiles[2][1].owner == -1 \
            and self.tiles[3][2].owner == -1 and self.tiles[4][2].owner == -1:
                return 1 if player == -1 else -1
        if self.tiles[3][0].wallDirection == 3 and self.tiles[4][1].wallDirection == 4:
            # Check if player 2 owns all the tiles walling in player 1
            if self.tiles[3][0].owner == -1 and self.tiles[4][1].owner == -1:
                return 1 if player == -1 else -1
        # No player has been walled in
        return 0

    def get_tilesOwned_dif(self, player):
        '''
        Returns the difference in tiles owned by player compared to the other player
        '''
        return self._get_this_player(player).numTilesOwned - \
            self._get_other_player(player).numTilesOwned

    def _get_this_player(self, player):
        '''
        Returns the Player object with the same playerID as player
        '''
        if self.tiles[self.n-1][0].playerID == player:
            return self.tiles[self.n-1][0]
        else:
            return self.tiles[0][self.n-1]
    
    def _get_other_player(self, player):
        '''
        Returns the Player object with a different playerID than player
        '''
        if self.tiles[self.n-1][0].playerID == player:
            return self.tiles[0][self.n-1]
        else:
            return self.tiles[self.n-1][0]

    def swap_all_tile_owners(self):
        '''
        Swaps the ownership of all tiles on the board
        Used to get the canonical form in KindoGame
        '''
        for x in range(self.n):
            for y in range(self.n):
                if self.tiles[x][y].owner == 1:
                    self.tiles[x][y].owner = -1
                elif self.tiles[x][y].owner == -1:
                    self.tiles[x][y].owner = 1

class Tile:
    '''
    Class used to represent the tiles on the board
    '''
    def __init__(self, owner, wallDirection, hasDot, isKing, isUnwallable, \
        playerID, movesCurrent, movesNext, numTilesOwned):
        '''
        Initializes a Tile object
        [In] owner: player id of player who owns tile (0: none, 1: p1, -1: p2)
        [In] wall: 0 if no wall on this tile, else 1 if N, 2 if E, 3 if S, 4 if W
        [In] hasDot: true if owner captured tile on previous turn until owner's next turn
        [In] isKing: true if tile is a king tile
        [In] isUnwallable: true if wall cannot be placed on this tile
        '''
        self.owner = owner
        self.wallDirection = wallDirection
        self.hasDot = hasDot
        self.isKing = isKing
        self.isUnwallable = isUnwallable
        # Player attributes will be stored in Tile instead of player class.
        # (Refer to Player class for attribute details)
        # Player 1's King tile will store Player 1's info for update and retrieval
        # Player 2's King tile will store Player 2's info for update and retrieval
        # Although logically it makes more sense to have a separate Player class
        # instead of EVERY tile having player info, to work with this framework without 
        # making excessive changes, this somewhat less intuitive approach is used.
        self.playerID = playerID
        self.movesCurrent = movesCurrent
        self.movesNext = movesNext
        self.numTilesOwned = numTilesOwned

# class Player():
#     '''
#     Class used to represent player info
#     '''
#     def __init__(self, playerID, movesCurrent, movesNext, numTilesOwned):
#         '''
#         [In] playerID: number to identify the player
#         [In] movesCurrent: number of moves player has remaining in current turn
#         [In] movesNext: number of moves player will have at start of their next turn
#         [In] numTilesOwned: number of tiles owned by the player
#         '''
#         self.playerID = playerID
#         self.movesCurrent = movesCurrent
#         self.movesNext = movesNext
#         self.numTilesOwned = numTilesOwned
        