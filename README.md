# Alpha Zero General Implementation of Kindo

This is an implementation of the game Kindo in the Alpha Zero General framework.

## File Explanation

The following is a brief description of all files implemented specifically for Kindo:

* mainKindo.py:  
* pitKindo.py: Used to pit two players (humans or AI agents) against each other using the Arena.py Arena class
* KindoPlayers.py: Defines each type of player (human and AI agent) and how each player chooses an action based on the valid action for a given board state
* KindoLogic.py: Manages the board (state) logic for Kindo by updating and retrieving values from the board
* KindoGame.py: Calls the appropriate methods in KindoLogic.py when required by the game (intermediary between KindoLogic.py and Arena.py)

Other files used by Kindo that are part of the Alpha Zero General framework:

* Arena.py: Plays games between two players by making the appropriate calls to KindoPlayer.py to choose actions and KindoGame.py to get the next state given the chosen action
* Coach.py: Executes self-play learning

I have provided detailed comments in most of these files for a more thorough understanding of how each file operates.

## How to Train

In the mainKindo.py file, set the args to the values desired for training.

Once you have chosen the desired args, run the following command to begin the training:

```
python mainKindo.py
```

mainKindo.py process:

* Create g, an instance of KindoGame (implementation in KindoGame.py)
* Create nnet, an instance of NNetWrapper (implementation in Kindo's NNet.py) using KindoGame g
* If flag set, nnet loads model from checkpoint, otherwise nnet starts a new one
* Create c, an instance of Coach (implementation in Coach.py) using KindoGame g, NNetWrapper nnet, and mainKindo.py's args
* If flag set, c loads training examples, otherwise starts with no examples
* Start learning with the Kindo game object and Kindo neural net using Coach's learn() method

Coach.learn() process:

* 

## How to Play

In the pitKindo.py file, set the following variables to the integer values corresponding to what kind of players you want to be in the game:

* player1_type = 
* player2_type =

The player types are:

* (0) hp = Human player
* (1) nn = AI trained through a neural network
* (2) gp = AI which acts through a simple evaluation method
* (3) rp = AI which acts randomly

Once you have set the players you wish to use, simply run the following command:

```
python pitKindo.py
```

This will play two games with each player starting one game as player 1 and one game as player 2.

Note: You can also play the game with two human players at http://www.playkindo.com

## Game Rules

**Goal**

Capture the opponent's King tile to win the game.

**Turn**

Each turn you are given 2 moves by default (up to 4 moves maximum if awarded bonus moves).
You can use each of your moves to perform one of the following actions:

* Convert a neutral tile which is horizontally or vertically adjacent to a tile you control
* Capture an enemy tile which is horizontally or vertically adjacent to a tile you control
* Place a wall on a tile you already control (if that tile already has a wall, your move will be used to change the direction of the wall)

**Walls**

Normally you can capture an enemy tile as long as it is horizontally or vertically adjacent to a tile you control. However, if the enemy tile has a wall on the side your adjacent tile is on, it blocks you from capturing that enemy tile from that direction.

NOTE: Walls cannot be placed on the tiles located on the diagonal from the top left to the bottom right. These tiles have a "bracket" image as a reminder that walls cannot be placed there.

**Mass Capture**

When you capture an enemy tile, if it results in any of their tiles being isolated from their King (no path of friendly tiles leading back to their king), those tiles will also be captured.

**Last Played**

When you play a tile, it will be marked with a small square in the center. This means that you played the tile during your last turn. At the start of your turn, this square will be removed. The reason these squares are marked will be explained in the "Bonus Moves" section.

**Bonus Moves**

You can earn multiple bonus moves during a single turn but may have no more than 4 moves total.
There are two ways to earn bonus moves:

* If you perform a "Mass Capture" (isolate enemy tiles)
* If your opponent captures a tile you played during your last turn (a tile marked with a square in the center)

NOTE: Bonus moves always apply to your next turn, not your current turn.

## Game Depiction

When playing using pit.py, the game tiles are depicted as follows:

    BOARD
            0       1       2       3       4    
        -----------------------------------------
        |       |       |       |       |       |
     0  |       |       |       |       |       |
        |       |       |       |       |       |
        -----------------------------------------
        |       |       |       |       |       |
     1  |       |       |       |       |       |
        |       |       |       |       |       |
        -----------------------------------------
        |       |       |       |       |       |
     2  |       |       |       |       |       |
        |       |       |       |       |       |
        -----------------------------------------
        |       |       |       |       |       |
     3  |       |       |       |       |       |
        |       |       |       |       |       |
        -----------------------------------------
        |       |       |       |       |       |
     4  |       |       |       |       |       |
        |       |       |       |       |       |
        ----------------------------------------- 

    NEUTRAL TILE
    ---------
    |       |
    |       |
    |       |
    ---------

    UNWALLABLE NEUTRAL TILE
    ---------
    | .   . |
    |       |
    | .   . |
    ---------

    P1 NO WALL

    ---------
    |       |
    |   x   |
    |       |
    ---------

    P1 NO WALL (PLAYED WITH-IN LAST TURN)

    ---------
    |   -   |
    | - x - |
    |   -   |
    ---------

    P1 WALL NORTH
    ---------
    | ..... |
    |   x   |
    |       |
    ---------

    P1 WALL EAST
    ---------
    |     : |
    |   x : |
    |     : |
    ---------

    P1 WALL SOUTH
    ---------
    |       |
    |   x   |
    | ..... |
    ---------

    P1 WALL WEST
    ---------
    | :     |
    | : x   |
    | :     |
    ---------

    P2 tiles are the same but with o instead of x

## Credits
[Daniel Scalettar](https://github.com/scalettar/)

* Implementation of Kindo in Alpha Zero General

[Paul Vauvrey](http://www.pvauvrey.com/)

* Original Kindo game design

[Alpha Zero General Repository](https://github.com/suragnair/alpha-zero-general)

* Original implementation of Alpha Zero General
  