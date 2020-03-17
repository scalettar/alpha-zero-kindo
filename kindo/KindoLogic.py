'''
Author: Daniel Scalettar (https://github.com/scalettar/)
Date: March, 2020
'''
    
class Board():
    '''
    This class specifies the board for Kindo.

    Board properties:
        board[x][y], x indexes columns, y indexes rows, (0, 0) is top left
        values: 1 = player 1, -1 = player 2, 0 = neutral
    '''
    def __init__(self, n):
        """
        Initializes starting board state
        """
        self.n = n
        # Create the board array of Tile objects
        self.tiles = [[Tile(0, 0, False, False, False) for i in range(self.n)] \
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
        # Create Player objects
        self.player1 = Player(1, 1, 2, 1)
        self.player2 = Player(-1, 0, 2, 1)

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
                if self.tiles[x][y].owner == player and (not self.tiles[x][y].isUnwallable):
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

class Tile:
    '''
    Class used to represent the tiles on the board
    '''
    def __init__(self, owner, wallDirection, hasDot, isKing, isUnwallable):
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

class Player():
    '''
    Class used to represent player info
    '''
    def __init__(self, playerID, movesCurrent, movesNext, numTilesOwned):
        '''
        [In] playerID: number to identify the player
        [In] movesCurrent: number of moves player has remaining in current turn
        [In] movesNext: number of moves player will have at start of their next turn
        [In] numTilesOwned: number of tiles owned by the player
        '''
        self.playerID = playerID
        self.movesCurrent = movesCurrent
        self.movesNext = movesNext
        self.numTilesOwned = numTilesOwned