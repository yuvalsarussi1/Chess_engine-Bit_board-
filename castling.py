import bitboard as b
import moves as mo
import threats as th
import board as bo
import castling as ca
import move_record as mr

def Piece_moved(from_sq: int,moved_piece: int):
    if moved_piece not in (b.WK,b.WR,b.BK,b.BR): return False
    
    if moved_piece == b.WK:
        b.CASTLING_WK = False
        b.CASTLING_WQ = False
    if moved_piece == b.BK:
        b.CASTLING_BK = False
        b.CASTLING_BQ = False
    
    
    if moved_piece == b.WR and from_sq == 0:
        b.CASTLING_WQ = False
    if moved_piece == b.WR and from_sq == 7:
        b.CASTLING_WK = False
    
    if moved_piece == b.BR and from_sq == 56:
        b.CASTLING_BQ = False
    if moved_piece == b.BR and from_sq == 63:
        b.CASTLING_BK = False
    


def Undo_piece_moved(from_sq: int,moved_piece: int,flags):
    if flags != mr.MoveRecord.CASTLE_FLAG: return False
    if moved_piece not in (b.WK,b.WR,b.BK,b.BR): return False

    if moved_piece == b.WK:
        b.WHITE_KING_MOVE = 0
    if moved_piece == b.BK:
        b.BLACK_KING_MOVE = 0
    if moved_piece == b.WR and from_sq == 0:
        b.WHITE_LR_MOVE = 0
    if moved_piece == b.WR and from_sq == 7:
        b.WHITE_RR_MOVE = 0

    if moved_piece == b.BR and from_sq == 56:
        b.BLACK_LR_MOVE = 0
    if moved_piece == b.BR and from_sq == 63:
        b.BLACK_RR_MOVE = 0



def castling_condition_King_side(square_num) -> bool:
    num = b.SQUARE_MAP[square_num]
    if num == b.WK:  
        if not b.CASTLING_WK: return False
        if b.ALL_OCCUPANCY & b.WHITE_KINGSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_black(4): return False
        if th.Threats.square_attacked_by_black(5): return False
        if th.Threats.square_attacked_by_black(6): return False
        
        return True

    elif num == b.BK:  # Black
        if not b.CASTLING_BK: return False
        if b.ALL_OCCUPANCY & b.BLACK_KINGSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_white(60): return False  
        if th.Threats.square_attacked_by_white(61): return False  
        if th.Threats.square_attacked_by_white(62): return False  
        
        return True

    return False



def castling_condition_Queen_side(side) ->bool:
    if side == 0:  
        if not b.CASTLING_WQ: return False
        if b.ALL_OCCUPANCY & b.WHITE_QUEENSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_black(4): return False  
        if th.Threats.square_attacked_by_black(3): return False  
        if th.Threats.square_attacked_by_black(2): return False  
        
        return True

    elif side == 1:  # Black
        if not b.CASTLING_BQ: return False
        if b.ALL_OCCUPANCY & b.BLACK_QUEENSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_white(60): return False  
        if th.Threats.square_attacked_by_white(59): return False  
        if th.Threats.square_attacked_by_white(58): return False  
        
        return True

    return False


def Execute_castling(side: int, kingside: bool):

    if side == 0:  # White
        if kingside:
            # King: e1 → g1
            b.PIECE_DICT[b.WK] &= ~(1 << 4)
            b.PIECE_DICT[b.WK] |=  (1 << 6)
            b.SQUARE_MAP[4] = b.E
            b.SQUARE_MAP[6] = b.WK
            b.WHITE_OCCUPANCY ^= (1 << 4)
            b.WHITE_OCCUPANCY |= (1 << 6)
            b.WHITE_KING_SQ = 6

            # Rook: h1 → f1
            b.PIECE_DICT[b.WR] &= ~(1 << 7)
            b.PIECE_DICT[b.WR] |=  (1 << 5)
            b.SQUARE_MAP[7] = b.E
            b.SQUARE_MAP[5] = b.WR
            b.WHITE_OCCUPANCY ^= (1 << 7)
            b.WHITE_OCCUPANCY |= (1 << 5)

        else:  # Queenside
            # King: e1 → c1
            b.PIECE_DICT[b.WK] &= ~(1 << 4)
            b.PIECE_DICT[b.WK] |=  (1 << 2)
            b.SQUARE_MAP[4] = b.E
            b.SQUARE_MAP[2] = b.WK
            b.WHITE_OCCUPANCY ^= (1 << 4)
            b.WHITE_OCCUPANCY |= (1 << 2)
            b.WHITE_KING_SQ = 2

            # Rook: a1 → d1
            b.PIECE_DICT[b.WR] &= ~(1 << 0)
            b.PIECE_DICT[b.WR] |=  (1 << 3)
            b.SQUARE_MAP[0] = b.E
            b.SQUARE_MAP[3] = b.WR
            b.WHITE_OCCUPANCY ^= (1 << 0)
            b.WHITE_OCCUPANCY |= (1 << 3)

    else:  # Black
        if kingside:
            # King: e8 → g8
            b.PIECE_DICT[b.BK] &= ~(1 << 60)
            b.PIECE_DICT[b.BK] |=  (1 << 62)
            b.SQUARE_MAP[60] = b.E
            b.SQUARE_MAP[62] = b.BK
            b.BLACK_OCCUPANCY ^= (1 << 60)
            b.BLACK_OCCUPANCY |= (1 << 62)
            b.BLACK_KING_SQ = 62

            # Rook: h8 → f8
            b.PIECE_DICT[b.BR] &= ~(1 << 63)
            b.PIECE_DICT[b.BR] |=  (1 << 61)
            b.SQUARE_MAP[63] = b.E
            b.SQUARE_MAP[61] = b.BR
            b.BLACK_OCCUPANCY ^= (1 << 63)
            b.BLACK_OCCUPANCY |= (1 << 61)

        else:  # Queenside
            # King: e8 → c8
            b.PIECE_DICT[b.BK] &= ~(1 << 60)
            b.PIECE_DICT[b.BK] |=  (1 << 58)
            b.SQUARE_MAP[60] = b.E
            b.SQUARE_MAP[58] = b.BK
            b.BLACK_OCCUPANCY ^= (1 << 60)
            b.BLACK_OCCUPANCY |= (1 << 58)
            b.BLACK_KING_SQ = 58

            # Rook: a8 → d8
            b.PIECE_DICT[b.BR] &= ~(1 << 56)
            b.PIECE_DICT[b.BR] |=  (1 << 59)
            b.SQUARE_MAP[56] = b.E
            b.SQUARE_MAP[59] = b.BR
            b.BLACK_OCCUPANCY ^= (1 << 56)
            b.BLACK_OCCUPANCY |= (1 << 59)

def Restore_castling(moved_piece: int, to_sq: int):

    # White kingside: king e1↔g1, rook h1↔f1
    if moved_piece == b.WK and to_sq == 6:
        # King: g1 → e1
        b.PIECE_DICT[b.WK] ^= (1 << 6) | (1 << 4)
        b.SQUARE_MAP[6] = b.E
        b.SQUARE_MAP[4] = b.WK
        b.WHITE_OCCUPANCY ^= (1 << 6) | (1 << 4)
        b.WHITE_KING_SQ = 4

        # Rook: f1 → h1
        b.PIECE_DICT[b.WR] ^= (1 << 5) | (1 << 7)
        b.SQUARE_MAP[5] = b.E
        b.SQUARE_MAP[7] = b.WR
        b.WHITE_OCCUPANCY ^= (1 << 5) | (1 << 7)

    # White queenside: king e1↔c1, rook a1↔d1
    elif moved_piece == b.WK and to_sq == 2:
        # King: c1 → e1
        b.PIECE_DICT[b.WK] ^= (1 << 2) | (1 << 4)
        b.SQUARE_MAP[2] = b.E
        b.SQUARE_MAP[4] = b.WK
        b.WHITE_OCCUPANCY ^= (1 << 2) | (1 << 4)
        b.WHITE_KING_SQ = 4

        # Rook: d1 → a1
        b.PIECE_DICT[b.WR] ^= (1 << 3) | (1 << 0)
        b.SQUARE_MAP[3] = b.E
        b.SQUARE_MAP[0] = b.WR
        b.WHITE_OCCUPANCY ^= (1 << 3) | (1 << 0)

    # Black kingside: king e8↔g8, rook h8↔f8
    elif moved_piece == b.BK and to_sq == 62:
        # King: g8 → e8
        b.PIECE_DICT[b.BK] ^= (1 << 62) | (1 << 60)
        b.SQUARE_MAP[62] = b.E
        b.SQUARE_MAP[60] = b.BK
        b.BLACK_OCCUPANCY ^= (1 << 62) | (1 << 60)
        b.BLACK_KING_SQ = 60

        # Rook: f8 → h8
        b.PIECE_DICT[b.BR] ^= (1 << 61) | (1 << 63)
        b.SQUARE_MAP[61] = b.E
        b.SQUARE_MAP[63] = b.BR
        b.BLACK_OCCUPANCY ^= (1 << 61) | (1 << 63)

    # Black queenside: king e8↔c8, rook a8↔d8
    elif moved_piece == b.BK and to_sq == 58:
        # King: c8 → e8
        b.PIECE_DICT[b.BK] ^= (1 << 58) | (1 << 60)
        b.SQUARE_MAP[58] = b.E
        b.SQUARE_MAP[60] = b.BK
        b.BLACK_OCCUPANCY ^= (1 << 58) | (1 << 60)
        b.BLACK_KING_SQ = 60

        # Rook: d8 → a8
        b.PIECE_DICT[b.BR] ^= (1 << 59) | (1 << 56)
        b.SQUARE_MAP[59] = b.E
        b.SQUARE_MAP[56] = b.BR
        b.BLACK_OCCUPANCY ^= (1 << 59) | (1 << 56)

    # Recompute all occupancy
    # b.ALL_OCCUPANCY = b.WHITE_OCCUPANCY | b.BLACK_OCCUPANCY

def castling_trigger(from_sq: int,to_sq: int,moved_piece: int):
    if moved_piece == b.WK and from_sq == 4 and to_sq == 6:
        Execute_castling(0, kingside=True)
    elif moved_piece == b.WK and from_sq == 4 and to_sq == 2:
        Execute_castling(0, kingside=False)
    elif moved_piece == b.BK and from_sq == 60 and to_sq == 62:
        Execute_castling(1, kingside=True)
    elif moved_piece == b.BK and from_sq == 60 and to_sq == 58:
        Execute_castling(1, kingside=False)

def Castling_execute(moved_piece, flags,to_sq):
    if moved_piece == b.WK:
        ca.Execute_castling(0, kingside=(to_sq == 6))
    else:
        ca.Execute_castling(1, kingside=(to_sq == 62))

