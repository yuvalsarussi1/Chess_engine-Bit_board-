import bitboard as b
import moves as mo
import threats as th
import board as bo
import castling as ca
import move_record as mr

def Piece_moved(from_sq: int,moved_piece: int):
    if moved_piece not in (b.WK,b.WR,b.BK,b.BR): return False
    
    if moved_piece == b.WK:
        b.WHITE_KING_MOVE = 1

    if moved_piece == b.BK:
        b.BLACK_KING_MOVE = 1

    if moved_piece == b.WR and from_sq == 0:
        b.WHITE_LR_MOVE = 1
    if moved_piece == b.WR and from_sq == 7:
        b.WHITE_RR_MOVE = 1
    
    if moved_piece == b.BR and from_sq == 56:
        b.BLACK_LR_MOVE = 1
    if moved_piece == b.BR and from_sq == 63:
        b.BLACK_RR_MOVE = 1
    



def castling_condition_King_side(square_num) -> bool:
    num = b.SQUARE_MAP[square_num]
    if num == b.WK:  
        if b.WHITE_KING_MOVE or b.WHITE_RR_MOVE: return False
        if b.ALL_OCCUPANCY & b.WHITE_KINGSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_black(4): return False  
        if th.Threats.square_attacked_by_black(5): return False  
        if th.Threats.square_attacked_by_black(6): return False  
        
        return True

    elif num == b.BK:  # Black
        if b.BLACK_KING_MOVE or b.BLACK_RR_MOVE: return False
        if b.ALL_OCCUPANCY & b.BLACK_KINGSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_white(60): return False  
        if th.Threats.square_attacked_by_white(61): return False  
        if th.Threats.square_attacked_by_white(62): return False  
        
        return True

    return False



def castling_condition_Queen_side(side) ->bool:
    if side == 0:  
        if b.WHITE_KING_MOVE or b.WHITE_LR_MOVE: return False
        if b.ALL_OCCUPANCY & b.WHITE_QUEENSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_black(4): return False  
        if th.Threats.square_attacked_by_black(3): return False  
        if th.Threats.square_attacked_by_black(2): return False  
        
        return True

    elif side == 1:  # Black
        if b.BLACK_KING_MOVE or b.BLACK_LR_MOVE: return False
        if b.ALL_OCCUPANCY & b.BLACK_QUEENSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_white(60): return False  
        if th.Threats.square_attacked_by_white(59): return False  
        if th.Threats.square_attacked_by_white(58): return False  
        
        return True

    return False



def Execute_castling(side: int, kingside: bool):
    # print("executing castling")
    if side == 0:  # White
        if kingside:
            # Move rook from h1 → f1
            b.PIECE_DICT[b.WR] &= ~(1 << 7)   # clear h1
            b.PIECE_DICT[b.WR] |=  (1 << 5)   # set f1
            b.SQUARE_MAP[7] = b.E
            b.SQUARE_MAP[5] = b.WR
            b.WHITE_OCCUPANCY ^= (1 << 7)
            b.WHITE_OCCUPANCY |= (1 << 5)
        else:
            # Move rook from a1 → d1
            b.PIECE_DICT[b.WR] &= ~(1 << 0)   # clear a1
            b.PIECE_DICT[b.WR] |=  (1 << 3)   # set d1
            b.SQUARE_MAP[0] = b.E
            b.SQUARE_MAP[3] = b.WR
            b.WHITE_OCCUPANCY ^= (1 << 0)
            b.WHITE_OCCUPANCY |= (1 << 3)

    else:  # Black
        if kingside:
            # Move rook from h8 → f8
            b.PIECE_DICT[b.BR] &= ~(1 << 63)  # clear h8
            b.PIECE_DICT[b.BR] |=  (1 << 61)  # set f8
            b.SQUARE_MAP[63] = b.E
            b.SQUARE_MAP[61] = b.BR
            b.BLACK_OCCUPANCY ^= (1 << 63)
            b.BLACK_OCCUPANCY |= (1 << 61)
        else:
            # Move rook from a8 → d8
            b.PIECE_DICT[b.BR] &= ~(1 << 56)  # clear a8
            b.PIECE_DICT[b.BR] |=  (1 << 59)  # set d8
            b.SQUARE_MAP[56] = b.E
            b.SQUARE_MAP[59] = b.BR
            b.BLACK_OCCUPANCY ^= (1 << 56)
            b.BLACK_OCCUPANCY |= (1 << 59)
    b.ALL_OCCUPANCY = b.WHITE_OCCUPANCY | b.BLACK_OCCUPANCY

    





def Restore_castling(moved_piece: int, to_sq: int):
    # print("restoring castling")
    # print(moved_piece,to_sq,"RESTORE CASTLING")



    if moved_piece == b.WK and to_sq == 6:   
        # rook: f1 -> h1
        b.SQUARE_MAP[7] = b.WR
        b.SQUARE_MAP[5] = b.E
        b.PIECE_DICT[b.WR] ^= (1 << 5) | (1 << 7)  
        b.WHITE_OCCUPANCY ^= (1 << 5) | (1 << 7)
        b.ALL_OCCUPANCY  ^= (1 << 5) | (1 << 7)

    elif moved_piece == b.WK and to_sq == 2: 
        # rook: d1 -> a1
        b.SQUARE_MAP[0] = b.WR
        b.SQUARE_MAP[3] = b.E
        b.PIECE_DICT[b.WR] ^= (1 << 0) | (1 << 3)
        b.WHITE_OCCUPANCY ^= (1 << 0) | (1 << 3)
        b.ALL_OCCUPANCY  ^= (1 << 0) | (1 << 3)

    elif moved_piece == b.BK and to_sq == 62: 
        # rook: f8 -> h8
        b.SQUARE_MAP[63] = b.BR
        b.SQUARE_MAP[61] = b.E
        b.PIECE_DICT[b.BR] ^= (1 << 61) | (1 << 63)
        b.BLACK_OCCUPANCY ^= (1 << 61) | (1 << 63)
        b.ALL_OCCUPANCY  ^= (1 << 61) | (1 << 63)

    elif moved_piece == b.BK and to_sq == 58: 
        # rook: d8 -> a8
        b.SQUARE_MAP[56] = b.BR
        b.SQUARE_MAP[59] = b.E
        b.PIECE_DICT[b.BR] ^= (1 << 56) | (1 << 59)
        b.BLACK_OCCUPANCY ^= (1 << 56) | (1 << 59)
        b.ALL_OCCUPANCY  ^= (1 << 56) | (1 << 59)





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
    if flags == mr.MoveRecord.CASTLE_FLAG:
            if moved_piece == b.WK:
                ca.Execute_castling(0, kingside=(to_sq == 6))
            else:
                ca.Execute_castling(1, kingside=(to_sq == 62))

