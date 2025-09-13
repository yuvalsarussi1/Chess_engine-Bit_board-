import moves as mo
import bitboard as b
import legal_moves as le
from board import *

MOVES_DICT = {}    
def All_Move_generate():
    global MOVES_DICT
    MOVES_DICT = {}   
    for sym in b.PIECES_TURN:                               # List of pieces for spacific turn
        piece_mask = b.PIECE_DICT[sym]                  # Coords based on symbol(can be more then one)
        while piece_mask:
            lsb = piece_mask & -piece_mask
            sq = lsb.bit_length() - 1
            piece_mask ^= lsb
            moves = mo.Piece_move(sq)
            MOVES_DICT[sq] = moves



