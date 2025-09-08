import bitboard as b
import moves as mo
from board import *

PIECE_NAMES = {
    b.WP: "P", b.WN: "N", b.WB: "B", b.WR: "R", b.WQ: "Q", b.WK: "K",
    b.BP: "p", b.BN: "n", b.BB: "b", b.BR: "r", b.BQ: "q", b.BK: "k",
    b.E:  "."
}


def iter_bits(mask: int):
    while mask:
        lsb = mask & -mask
        yield lsb.bit_length() - 1   # directly compute index
        mask ^= lsb

def index_to_square(index: int) -> str:
    file = chr((index % 8) + ord('a'))
    rank = str((index // 8) + 1)
    return file + rank

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
    
            # if moves:
            #     move_list = list(iter_bits(moves))
            #     piece_name = PIECE_NAMES.get(sym, str(sym))
            #     print(f"{piece_name} at {index_to_square(sq)} → {[index_to_square(m) for m in move_list]}")

def Has_legal_move(side):
    legal_moves = 0
    for from_sq,from_mask in MOVES_DICT.items():
        for to_sq in iter_bits(from_mask):
            Board.Move_attacker(from_sq,to_sq)
            if not Board.Check_state(side):
                legal_moves += 1
            Board.Undo_move()

    return legal_moves

def Has_legal_move_no_counter(side):
    for from_sq, from_mask in MOVES_DICT.items():
        m = from_mask
        while m:
            lsb = m & -m
            to_sq = lsb.bit_length() - 1
            m ^= lsb

            Board.Move_attacker(from_sq, to_sq)
            if not Board.Check_state(side):
                Board.Undo_move()
                return True
            Board.Undo_move()
    return False
