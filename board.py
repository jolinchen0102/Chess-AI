import rules
import ai

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Board(rules.RulesEnforcer,ai.AI):
    def __init__(self, ai_depth):
        """
        Creates a chessboard with pieces
        
        params: (ai_depth) max number of moves to search into 
        
        Notation:
        ------------
        "0-0": empty space  
        "b-p": black pawn
        "b-r": black rook
        "b-n": black knight
        "b-b": black bishop
        "b-q": black queen
        "b-k": black king  
        "w-k": white king
        """
        
        ai.AI.__init__(self, ai_depth)
        rules.RulesEnforcer.__init__(self)

        self.ai_depth = ai_depth
        
        #initialize the chessboard
        self.chessboard = [["0-0"]*8 for i in range(8)]
        
        #track which pieces have been taken
        self.white_taken = []
        self.black_taken = []
        
        #track which moves have been made in the game, key: move number, value: len 2 list of white and black move
        self.moves_made = {}
        
        #track the number of moves made
        self.move_count = 0
        
        #track whose turn it is (white always starts)
        self.current_turn = "w"
        
        #create pawns
        for i in range(8):
            self.chessboard[1][i] = 'b-p'
            self.chessboard[6][i] = 'w-p'
        
        #create rooks
        self.chessboard[0][0] = 'b-r'
        self.chessboard[0][7] = 'b-r'
        self.chessboard[7][0] = 'w-r'
        self.chessboard[7][7] = 'w-r'
        
        #create knights
        self.chessboard[0][1] = 'b-n'
        self.chessboard[0][6] = 'b-n'
        self.chessboard[7][1] = 'w-n'
        self.chessboard[7][6] = 'w-n'
        
        #create bishops
        self.chessboard[0][2] = 'b-b'
        self.chessboard[0][5] = 'b-b'
        self.chessboard[7][2] = 'w-b'
        self.chessboard[7][5] = 'w-b'
        
        #create queen and king
        self.chessboard[0][3] = 'b-q'
        self.chessboard[0][4] = 'b-k'
        self.chessboard[7][3] = 'w-q'
        self.chessboard[7][4] = 'w-k'

        self.game_over = False
            
    def print_board(self):
        """
        print the current board
        """
        for i in range(len(self.chessboard)):
            print("%d|"%(8-i)),
            for j in self.chessboard[i]:
                if j.split('-')[0] == 'b': print(bcolors.OKCYAN + j + bcolors.ENDC),
                elif j.split('-')[0] == 'w': print(bcolors.WARNING + j + bcolors.ENDC),
                else: print(j),
            print
            # print ("%d| "%(8-i) +' '.join(self.chessboard[i]))
        print(" "*3 + "-"*31)
        print("    a   b   c   d   e   f   g   h\n")

    def whose_turn(self):
        return self.current_turn

    
    def recommend_move(self, depth_override = None):
        """
        Call minimax function to generate best moves
        """
        if not depth_override:
            depth_override = self.ai_depth

        self.get_successor(depth_override)
        return self.minimaxRoot(depth_override, self.initial_state, True)
    def make_move_ai(self, depth_override = None):
        """
        Let the AI make the move
        """
        if not depth_override:
            depth_override = self.ai_depth

        myoutput = self.recommend_move(depth_override)
        start  = myoutput[1]
        finish = myoutput[2]

        self.make_move(start, finish)
        print("AI moves from %s to %s\n"%(str(start), ''.join(str(x) for x in finish)))
        
        return self.chessboard


    def make_move(self, start, finish):
        """
        Make a move
        
        input:
        starting coordinate: example "e4"
        ending coordinate: example "e5"
        
        output:
        "Move success" or "Move invalid", self.chessboard is updated with the move made
        
        Uses the rules.RulesEnforcer() to make sure that the move is valid
        
        """
        
        #map start and finish to gameboard coordinates
        start  = rules.RulesEnforcer.coordinate_mapper(start)
        finish = rules.RulesEnforcer.coordinate_mapper(finish)
        
        #need to move alot of this logic to the rules enforcer
        start_cor0  = start[0]
        start_cor1  = start[1]
        
        finish_cor0 = finish[0]
        finish_cor1 = finish[1]
        
        #check if destination is white, black or empty
        start_color = self.chessboard[start_cor0][start_cor1].split('-')[0]
        start_piece = self.chessboard[start_cor0][start_cor1].split('-')[1]
        
        #check if destination is white, black or empty
        destination_color = self.chessboard[finish_cor0][finish_cor1].split('-')[0]
        destination_piece = self.chessboard[finish_cor0][finish_cor1].split('-')[1]
        
        #cannot move if starting square is empty
        if start_color == '0':
            return bcolors.FAIL+ "Starting position is empty!" + bcolors.ENDC
        
        #cannot move the other person's piece
        if self.current_turn != start_color:
            return bcolors.FAIL+"Cannot move your opponent's piece!"+bcolors.ENDC
        
        #cannot take your own piece 
        if self.current_turn == destination_color:
            return bcolors.FAIL+"Invalid move, cannot take your own piece!"+bcolors.ENDC
        elif self.current_turn != destination_color and destination_color != '0':
            if destination_piece == 'k':
                self.game_over = True
                if self.current_turn == 'w': print(bcolors.HEADER+"Congratulation, You won!")
                else: print(bcolors.HEADER+"Robot wins"+bcolors.ENDC)
                return
            elif self.current_turn == 'w':
                self.black_taken.append(destination_piece)
            elif self.current_turn == 'b':
                self.white_taken.append(destination_piece)     
        else:
            pass
        
        mypiece = self.chessboard[start_cor0][start_cor1]
        self.chessboard[start_cor0][start_cor1] = '0-0'
        self.chessboard[finish_cor0][finish_cor1] = mypiece
        
        #if the move is a success, change the turn state
        if self.current_turn == "w":
            self.current_turn = "b"
        elif self.current_turn == "b":
            self.current_turn = "w"
        
        return self.chessboard


    
    def current_position_score(self):
        """
        Get the position score of the current game being played
        """
        return self.position_evaluator(self.chessboard)


