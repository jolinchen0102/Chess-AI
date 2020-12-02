"""Main entry point into the game"""

import board
import re
import time

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
    
def check_input(point):
    pattern = re.compile("^[a-h][1-8]$")
    return pattern.match(point)

if __name__ == '__main__':

    current_game = board.Board(3)
    print("\n" + bcolors.HEADER + "Let's start the game, please input column followed by row (e.g. a2, b4) for the starting/ending coordinate:\n"+ bcolors.ENDC)
    current_game.print_board()

    while not current_game.game_over:
        print("It's your turn now: ")
        
        start_point = raw_input("Enter starting point coordinate (e.g. a2): ")
        while not check_input(start_point):
            print(bcolors.FAIL + "Please enter a valid position!" + bcolors.ENDC)
            start_point = raw_input("Enter starting point coordinate (e.g. a2): ")
        
        end_point = raw_input("Enter ending point coordinate (e.g. a4): ")
        while not check_input(end_point):
            print(bcolors.FAIL + "Please enter a valid position!" + bcolors.ENDC)
            end_point = raw_input("Enter ending point coordinate (e.g. a4): ")

        current_game.make_move(start_point,end_point)
        current_game.print_board()
        
        if current_game.current_turn == 'b':
            print("AI is making a move...")
            start = time.time()
            # Please change the number to change the search depth
            current_game.make_move_ai(3)
            elapsed_time_fl = (time.time() - start)/3
            current_game.print_board()
            print("average run time per move: ", elapsed_time_fl)
