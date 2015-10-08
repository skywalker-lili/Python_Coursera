"""
Mini-max Tic-Tac-Toe Player by Achen
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # see if the current board is a game end
    end = board.check_win()
    if end == provided.PLAYERX: # PLAYERX win
        score = SCORES[provided.PLAYERX]
        return tuple([score, (-1, -1)])
    elif end == provided.PLAYERO: # PLAYERO win
        score = SCORES[provided.PLAYERO]
        return tuple([score, (-1, -1)])
    elif end == provided.DRAW: # a draw
        score = SCORES[provided.DRAW]
        return tuple([score, (-1, -1)])
    
    # the game isn't over, use recursion to select the best move
    else: 
        scores = [] # a list to record scores for each possible move
        # Step 1: try each possible next moves
        moves = board.get_empty_squares() 
        for move in moves:
            board_cloned = board.clone()
            board_cloned.move(move[0], move[1], player)
            new_player = provided.switch_player(player) # switch player
            # Recursively use mm_move() to score the new cloned board
            score = mm_move(board_cloned, new_player)[0]
            scores.append(score)
            # Special cases: winning move is found during iterating
            if player == provided.PLAYERX and \
            score == SCORES[provided.PLAYERX]:
                return tuple([score, (move[0], move[1])])        
            # PLAYERX is playing and its winning move is found. Just return.
            
            elif player == provided.PLAYERO and \
            score == SCORES[provided.PLAYERO]:
                return tuple([score, (move[0], move[1])])
            # PLAYERO is playing and its winning move is found. Just return.
        
        # Step 2: among the scores and moves in the list "returns" find the
        # best one for the current player
        
        # if PLAYERO is playing, should minize the score
        if player == provided.PLAYERO:
            the_index = scores.index(min(scores))
        # if PLAYERX is playing, should maximize the score
        else:
            the_index = scores.index(max(scores))
        # finally return the move
        return tuple([scores[the_index], \
                      (moves[the_index][0], moves[the_index][1])])  
    
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
