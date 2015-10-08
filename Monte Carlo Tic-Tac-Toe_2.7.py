"""
Monte Carlo Tic-Tac-Toe Player by Achen
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 200         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here. 

# a helper function to return a random sqaure
def random_square(board):
    """
    Returns the position of a random empty square, given a board.
    Nothing happens if there isn't any empty square.
    """
    empty_squares = board.get_empty_squares()
    if len(empty_squares) > 0:
        return random.choice(empty_squares)   

# mc_update_scores(grid_score, board, player)
def mc_update_scores(grid_score, board, player):
    """
    Traverse the board and update the score board for the current player.
    If the game is a draw or not finished, do nothing.
    If the current player wins, "score_cur" will be added to squares
    occupied by the current player and "score_other" will be subtracted to
    squares occupied by the other player.
    If the current player loses, "score_cur" will be subtracted to her
    squares and "score_other" will be added to the oterh player's squares.
    """    
    dim = board.get_dim()
    winner = board.check_win()
    if winner == None or winner == provided.DRAW:
        pass
    else:
        if player == winner: # the current player is the winner!
            for dummy_row in range(dim):
                for dummy_column in range(dim):
                    if board.square(dummy_row, dummy_column) == player:
                    # add score for squares belonging to the winner
                        grid_score[dummy_row][dummy_column] += SCORE_CURRENT
                    elif board.square(dummy_row, dummy_column) == provided.EMPTY:
                        pass
                    else:
                    # subtract score for squares belonging to the loser
                        grid_score[dummy_row][dummy_column] -= SCORE_OTHER
        else: # the current player is the loser!
            for dummy_row in range(dim):
                for dummy_column in range(dim):
                    if board.square(dummy_row, dummy_column) == player:
                    # subtract score for squares belonging to the winner
                        grid_score[dummy_row][dummy_column] -= SCORE_CURRENT
                    elif board.square(dummy_row, dummy_column) == provided.EMPTY:
                        pass
                    else:
                    # subtract score for squares belonging to the loser
                        grid_score[dummy_row][dummy_column] += SCORE_OTHER

# mc_trial(board, player)
def mc_trial(board, player):
    """
    Play on current board and next player to finish by randomly choose
    squares. This functions modifies the board and returns nothing.
    """
    while board.check_win() == None and len(board.get_empty_squares()) > 0:
        position = random_square(board)
        board.move(position[0], position[1],\
                  player)
        # print(player, position)
        player = provided.switch_player(player)
    # print "----------"
        
# get_best_move(board, grid_score)
def get_best_move(board, grid_score):
    """
    Return the position of an empty square with highest score. When there
    are several these squares, randomly select one.
    """
    dim = board.get_dim()
    empty_squares = board.get_empty_squares()
    print empty_squares
    scores = []
    if len(empty_squares) == 0:
        pass
    else:
        for square in empty_squares:
            scores.append(grid_score[square[0]][square[1]])
        max_score = max(scores)
        # already has the maxmium score
        
        # find the moves of maximum score and then randomly select one
        best_moves = []
        for square in empty_squares:
            if grid_score[square[0]][square[1]] == max_score:
                best_moves.append(square)
        best_move = random.choice(best_moves)
        return best_move

# mc_move(board, player, trials)
def mc_move(board, player, trials):
    """
    Combine other methods written for machine player to output the 
    move it choose, given which player machine is playing on behalf, 
    the current board and the number of trials machine needs to 
    play before choose its best move.
    """
    # Step 0: Check whether the game is over; otherwise continue playing
    if board.check_win() != None:
        pass
    else:
        # Step 1: Runs trials and update the score board
        dim = board.get_dim()
        grid_score = [[0 for dummy_i in range(dim)] for dummy_j in range(dim)]
        for dummy_i in range(trials):
            board_trial = board.clone() 
        # each trial will play on its own cloned board
            mc_trial(board_trial, player) 
            mc_update_scores(grid_score, board_trial, player)
    
        # Step 2: find the best move based on latest score board
        best_move = get_best_move(board, grid_score)
        # Step 3: return the move
        return best_move


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)