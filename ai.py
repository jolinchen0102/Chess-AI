# Implementation of minimax algorithm
import math
import copy
import rules

class TreeNode(object):
    """Tree structure for storing possible chess positions

    self.data: chess position, evaluation score]
    """
    def __init__(self, data, parent=None):
        self.data = data
        self.children = []
        
    def add(self, data):
        self.children.append(TreeNode(data))

    def see_children(self):
        for i in self.children:
            print (i.data)

class AI(object):
    
    #set the value of each of the pieces to be used in the hard coded heuristic algorithm
    piecesValue = {'p':1,'r':10,'n':5,'b':5,'q':20,'k':100}
    
    def __init__(self, depth = 3):
        
        self.depth = depth
        self.initial_state = None

    @staticmethod
    def evaluate_board(board):
        """Heuristic function to evaluate the chess postion

        Args:
            board (8 x 8 2d array): chess board containing the postion of each pieces

        Returns:
            score (float): a float evaluating how good is the current board
            if score > 0, white is winning; otherwise, black is winning 
        """
        # initialize score to 0
        score = 0
        
        #loop through rows on the board and evaluate, special cases are considered
        for x, row in enumerate(board):
            for y, col in enumerate(row):
                color = col.split('-')[0]
                piece = col.split('-')[1]
                
                # add the value of all pieces
                if color == 'w':
                    score += AI.piecesValue[piece]
                elif color == 'b':
                    score -= AI.piecesValue[piece]

                # adjust score for forward pawn (more likely to castle)
                # plus .1 for each square that the pawn is advanced
                if piece == 'p' and color == 'w':
                    score += (8 - x - 2)*.02 
                if piece == 'p' and color == 'b':
                    score -= (x - 1)*.02
                    
                # adjust score for developed knights 
                # plus .1 for each square that the knight is advanced
                if piece == 'n' and color == 'w':
                    score += math.pow(1 + (8 - x - 1)*.05, 2)
                    # penalize if knights are on the sides of the board
                    if col == 0 or col == 7:
                        score -= .1
                if piece == 'n' and color == 'b':
                    score -= math.pow(1 + (x)*.05, 2)
                    # penalize if knights are on the sides of the board
                    if col == 0 or col == 7:
                        score -= .1

                # adjust score for bishops with open diagonals
                if piece == 'b' and color == 'w':
                    #check for open diagonals
                    new_row = x - 1
                    new_col = y + 1
                    while new_row >= 0 and new_col <= 7:
                        square = board[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            score += .05
                            new_row -= 1
                            new_col += 1
                            continue
                        elif piece.split('-')[0] == 'b':
                            score += .25
                            break
                        elif piece.split('-')[0] == 'w':
                            break

                if piece == 'b' and color == 'w':
                    #check for open diagonals
                    new_row = x - 1
                    new_col = y - 1
                    while new_row >= 0 and new_col >= 0:
                        square = board[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            score += .05
                            new_row -= 1
                            new_col -= 1
                            continue
                        elif piece.split('-')[0] == 'b':
                            score += .25
                            break
                        elif piece.split('-')[0] == 'w':
                            break

                #score adjustment for bishops with open diagonals
                if piece == 'b' and color == 'b':
                    #check for open diagonals
                    new_row = x + 1
                    new_col = y + 1
                    while new_row <= 7 and new_col <= 7:
                        square = board[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            score += .05
                            new_row -= 1
                            new_col += 1
                            continue
                        elif piece.split('-')[0] == 'w':
                            score += .25
                            break
                        elif piece.split('-')[0] == 'b':
                            break

                if piece == 'b' and color == 'b':
                    #check for open diagonals
                    new_row = x + 1
                    new_col = y - 1
                    while new_row <= 7 and new_col >= 0:
                        square = board[x][y]
                        #add points for open diagonals
                        if square == '0-0':
                            score += .05
                            new_row -= 1
                            new_col -= 1
                            continue
                        elif piece.split('-')[0] == 'w':
                            score += .25
                            break
                        elif piece.split('-')[0] == 'b':
                            break
        return round(score, 4)
       

    def get_successor(self, depth_override = None):
        """ function to generate ans set the successor of the current game state

        Returns:
            None, but set self.initial_state to fascilitate minimax search
        """
        #initialize the tree by putting the current state into the parent node of the chessboard. 
        self.initial_state = TreeNode([copy.deepcopy(self.chessboard)])
        current_positions = [self.initial_state]

        #track the number of moves into the future you are calculating.
        depth = 1

        #override the target depth if depth is explicitly defined
        target_depth = depth_override or self.depth

        #get the current turn
        current_turn = copy.copy(self.current_turn)

        while depth <= target_depth:
            for position in current_positions:
                #get a dictionary of possible chess moves
                pos_moves = rules.RulesEnforcer.all_possible_moves(position.data[0], current_turn)

                #generate all possible moves
                for start, moves in pos_moves.items():
                    for move in moves:
                        current_pos = position.data[0]
                        new_pos = AI.make_hypothetical_move(start, move, current_pos)

                        if depth > 1:
                            position.add([new_pos])
                        else:
                            position.add([new_pos, start, move])

            depth += 1

            #populate the new current positions list
            new_positions = []
            for position in current_positions:
                new_positions += position.children
            current_positions = new_positions
            
            #switch turn
            if current_turn == 'w':
                current_turn = 'b' 
            else:
                current_turn = 'w' 
    
    """IMPLEMENTATION OF MINIMAX WITH ALPHA-BETA PRUNING"""
    def minimaxRoot(self, depth, node, isMaximizing):
        bestMove = -1e8
        bestMoveFinal = None
        for child in node.children:
            value = max(bestMove, self.minimax(child, -1e8, 1e8, depth-1, not isMaximizing))
            if( value > bestMove):
                bestMove = value
                bestMoveFinal = child.data
        return bestMoveFinal
    
    def minimax(self, node, alpha, beta, depth, is_maximizing):
        if depth == 0:
            return AI.evaluate_board(node.data[0])
        if is_maximizing:
            bestMove = -1e8
            for child in node.children:
                bestMove = max(bestMove, self.minimax(child, alpha, beta, depth - 1, not is_maximizing))
                alpha = max(alpha,bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = 1e8
            for child in node.children:
                bestMove = min(bestMove, self.minimax(child, alpha, beta, depth - 1, not is_maximizing))
                beta = min(beta, bestMove)
                if(beta <= alpha):
                    return bestMove
            return bestMove

    @staticmethod
    def make_hypothetical_move(start, finish, chessboard):
        """
        Make a hypothetical move, this will be used to generate the possibilities to be
        stored in the chess tree
        
        input:
        starting coordinate: example "e4"
        ending coordinate: example "e5"
        chessboard: chessboard that you want to move
        
        output:
        "Move success" or "Move invalid"
        
        Uses the rules.RulesEnforcer() to make sure that the move is valid
        
        """
        #deepcopy the chessboard so that it does not affect the original
        mychessboard = copy.deepcopy(chessboard[:])
        
        #map start and finish to gameboard coordinates
        start  = rules.RulesEnforcer.coordinate_mapper(start)
        finish = rules.RulesEnforcer.coordinate_mapper(finish)
        
        #need to move alot of this logic to the rules enforcer
        start_cor0  = start[0]
        start_cor1  = start[1]
        
        finish_cor0 = finish[0]
        finish_cor1 = finish[1]
        
        #check if destination is white, black or empty
        start_color = mychessboard[start_cor0][start_cor1].split('-')[0]
        start_piece = mychessboard[start_cor0][start_cor1].split('-')[1]
        
        #check if destination is white, black or empty
        destination_color = mychessboard[finish_cor0][finish_cor1].split('-')[0]
        destination_piece = mychessboard[finish_cor0][finish_cor1].split('-')[1]
        
        #cannot move if starting square is empty
        if start_color == '0':
            return "Starting square is empty!"
        
        mypiece = mychessboard[start_cor0][start_cor1]
        mychessboard[start_cor0][start_cor1] = '0-0'
        mychessboard[finish_cor0][finish_cor1] = mypiece
        
        return mychessboard


   