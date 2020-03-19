import numpy as np

class HumanKindoPlayer():
    '''
    Action chosen by human
    '''
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        # Get list of valid moves
        validMoves = self.game.getValidMoves(board, 1)
        # Print list of valid moves
        for i in range(len(validMoves)):
            if validMoves[i]:
                x = int(i / (self.game.n * self.game.tileTypes))
                y = int((i % (self.game.n * self.game.tileTypes)) / self.game.tileTypes)
                w = (i % (self.game.n * self.game.tileTypes)) % self.game.tileTypes
                print("[", x, y, w, end=" ] ")
        # Player selects a move
        while True:
            playerInput = input()
            move = playerInput.split(" ")
            # Check input length is 3 (x, y, w)
            if len(move) == 3:
                # Input was correct length, check if valid input
                try:
                    x, y, w = [int(i) for i in move]
                    if ((0 <= x)) and (x < self.game.n) and \
                        (0 <= y) and (y < self.game.n) and \
                            (0 <= w) and (w < self.game.tileTypes):
                            action = (x * self.game.n * self.game.tileTypes) + \
                                (y * self.game.tileTypes) + w if x != -1 else \
                                    self.game.n ** 2
                            # Input was valid format, check if valid action
                            if validMoves[action]:
                                break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            # Move was invalid, try again
            print('Invalid move')
        # Return chosen action
        return action

class GreedyKindoPlayer():
    '''
    Action chosen based on best scoring action of all valid actions
    '''
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        # Get list of valid moves
        validMoves = self.game.getValidMoves(board, 1)
        # Empty list of candidate actions
        candidates = []
        # Iterate over all possible actions (valid and invalid)
        for action in range(self.game.getActionSize()):
            # Check if current action is invalid
            if validMoves[action] == 0:
                continue
            # Action is valid, get next board by applying current action to current board
            nextBoard, _ = self.game.getNextState(board, 1, action)
            # Evaluate score of next board state from applying current action
            score = self.game.getScore(nextBoard, 1)
            # Store score action pair in list of candidates
            candidates += [(-score, action)]
        # Sort list of candidate actions
        candidates.sort()
        # Return candidate action with best score
        return candidates[0][1]

class RandomPlayer():
    '''
    Action chosen randomly
    '''
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # Get list of valid moves
        validMoves = self.game.getValidMoves(board, 1)
        # Randomly pick an action
        action = np.random.randint(self.game.getActionSize())
        # Randomly pick actions until one is a valid move
        while validMoves[action] != 1:
            action = np.random.randint(self.game.getActionSize())
        # Return chosen action
        return action
