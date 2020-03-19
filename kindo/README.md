# Alpha Zero General Implementation of Kindo

This is an implementation of the game Kindo in the Alpha Zero General framework.

## How to Train

```
python main.py
```

## How to Play

In the pitKindo.py file, change the values of the following variables to choose what kind of players you want to be in the game:

* player1_type = <selection>
* player2_type = <selection>

A player can be a human or one of the following AI agents:

* nn = AI trained through a neural network
* gp = AI which acts through a simple evaluation method
* rp = AI which acts randomly

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

    P1 NO WALL

    ---------
    | x x x |
    | x   x |
    | x x x |
    ---------

    P1 NO WALL (PLAYED LAST)

    ---------
    | x x x |
    | x - x |
    | x x x |
    ---------

    P1 WALL NORTH
    ---------
    | ^ ^ ^ |
    | x   x |
    | x x x |
    ---------

    P1 WALL EAST
    ---------
    | x x > |
    | x   > |
    | x x > |
    ---------

    P1 WALL SOUTH
    ---------
    | x x x |
    | x   x |
    | v v v |
    ---------

    P1 WALL WEST
    ---------
    | < x x |
    | <   x |
    | < x x |
    ---------

    P1 UNWALLABLE
    ---------
    | . x . |
    | x   x |
    | . x . |
    ---------

    P2 tiles are the same but with o instead of x

## Credits
[Daniel Scalettar](https://github.com/scalettar/)
* Implementation of Kindo in Alpha Zero General
[Paul Vauvrey](http://www.pvauvrey.com/).
* Original game design

Original Alpha Zero General repository can be found [HERE](https://github.com/suragnair/alpha-zero-general)


