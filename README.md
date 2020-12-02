# Chess-AI

# Introduction

This project implements an AI game engine for chess. This has more com- plex rules and larger branching factor as high as 35, making it challenging to simulate the game, to evaluate states accurately and to search the game tree efficiently. To tackle the three problems, a simulator with simple command line interface is carefully designed; strategies are implemented to play against human player.

Greedy strategy is used as base case. To increase efficiency of game tree search, Minimax with $α − β\ P runing$ is implemented. Based on the analysis, the AI agent is evaluated against human player with satisfactory performance and efficiency.

# Simulator Design
 ## Tree-Based Game Design

Object Oriented approach is taken by the game implementation. Five classes are defined in the project: Piece, Board, AI, RulesEnforcer and TreeNode.

Piece is actually a summary of 6 classes, each represents a different type of pieces of the chess game (Pawn, Knight, Bishop etc.). It captures all the information needed to describe the 6 different types of piece of the chess game. Each class has a member function `moves()` to define the movement behavior for each of the different piece.

Board captures information needed to describe a game at a certain time point, an instance of Board is used to start and control the game. Firstly, it initializes a 8 * 8​ list of type char to represent the board of the game.

The pre-defined search depth is set to 3. Secondly, the class defines member functions make `move()` and make move `ai()` to move the chess piece and update the current board for the user and AI agent respectively. Notice that the member function recommend move() calls the successor moves generator and set to `self.state`, then returns the Minimax solution

RulesEnforcer is a class that defines all possible piece movements of the current board and other useful functions for the impletation of the game.

TreeNode stores all possible moves of a chess board in a tree struc- ture. If it is an internal node, node value is set as a length 1 list of the form `[board]`; if the node is a leaf node, it will contains further inform- ation about the starting and ending coordinates of the initial move that should be taken to reach that leaf node, it is a length 3 list of the form `[board, startingposition, endingposition]`.

AI is a class defined for the searching strategy. Methods such as evalu- ation function, successor function, Minimax and $\alpha − β\ Pruning$ are imple- mented in AI.

# AI Engine: Policy to Compute Next Move 

## Base Line: Greedy Expansion

Each pieces are assigned with a value indicating their importance: pawn=1, knight=5, bishop=5, rook=10, queen=50, king=500​. Greedy search tree expansion utilizes the class TreeNode to generates all possible moves of the current game state and store in its children list. The detailed implementation is listed below:

1. Initialize the root node of the tree by constructing a TreeNode with the value [self.chessboard] and set it to `self.initialstate`

2. Initialize depth = 1, construct a loop to keep searching and calling func- tion all possible `moves()` in the class RulesEnforcer to generate all possible moves for each pieces and append to the children list. Calling function make hypothetical `move()` to obtain the starting and ending coordinates for the leaf nodes. Iterate until depth > predefined depth​

3. Sets the generated game states (list of class TreeNode) to self.initial state in order to facilitate minimax search

   

##  Minimax with $α − β\ Pruning$

I extend the greedy game tree to a certain depth by using the standard Minimax search policy. An evaluation function of the state is defined. Apparently simply adding the value of each pieces is not enough, since even the same piece will exhibit different value at different positions. One example is that once a pawn gets closer to the opponent field, it becomes much more important because the probability of castling increase according to the game rule. Other rules are illustrated as follows:

1. Position of pawn: linear function, returned value is higher if the position of pawn is closer to the opponent’s side (more likely to castle)
2. Position of bishop: +0.05 if it is with open diagonal, +0.1 if it takes opponents piece
3. Position of knight: -0.1 if it is on the sides of the board and quadratic function returned higher value if the position is closer to the other sides

By function approximation, the evaluation of the state is defined to be the the sum of all pieces value from either side plus the evaluation of the board structure. The function returns positive value for the player’s side and neg- ative value for computer’s side.



# Instruction on Running the Game

To run the game, enter the following command: `python play.py`

