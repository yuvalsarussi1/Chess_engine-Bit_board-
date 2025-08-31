import bitboard as b
import moves as mo
from board import *



BIT_TO_INDEX = {1 << sq: sq for sq in range(64)}
def From_mask_to_coords(mask: int) ->int:
    coords = []
    while mask:
        lsb = mask & -mask
        coords.append(BIT_TO_INDEX[lsb])
        mask ^= lsb
    return coords


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






def Has_legal_move(side):
    legal_moves = []
    for from_sq,from_mask in MOVES_DICT.items():
        coords = From_mask_to_coords(from_mask)
        for to_sq in coords:
            moved_piece = b.SQUARE_MAP[from_sq] #can be str(piece_name)
            captured_piece = b.SQUARE_MAP[to_sq] #can be str(piece_name) or str(".")
 
            Board.Move_attacker(from_sq,to_sq)
            Board.Update_occupancy()
            th.Threats.threat_map_update()
            if not Board.Check_state(side):
                legal_moves.append((from_sq, to_sq))
                Board.Undo_move(from_sq,to_sq,moved_piece,captured_piece)
            Board.Undo_move(from_sq,to_sq,moved_piece,captured_piece)

    return len(legal_moves)
