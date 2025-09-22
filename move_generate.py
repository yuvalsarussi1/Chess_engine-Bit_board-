import moves as mo
import bitboard as b
import legal_moves as le
from board import *

#=== explanation for move_generate.py ===

# This module generates all possible moves for the current player in a chess game.
# It iterates through all pieces of the player whose turn it is, calculates their potential moves,
# and stores these moves in a dictionary for easy access.


MOVES_DICT = {}    
def All_Move_generate():
    # based on current turn, generate all possible moves for that side
    global MOVES_DICT
    MOVES_DICT = {}   
    for sym in b.PIECES_TURN:                               
        piece_mask = b.PIECE_DICT[sym]                  
        while piece_mask:
            lsb = piece_mask & -piece_mask
            sq = lsb.bit_length() - 1
            piece_mask ^= lsb
            moves = mo.Piece_move(sq)
            MOVES_DICT[sq] = moves
            


