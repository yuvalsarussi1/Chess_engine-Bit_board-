import bitboard as b
import moves as mo
import threats as th
import board as bo
import castling as ca
import move_record as mr

def Piece_moved(from_sq: int,to_sq: int,moved_piece: int,captured_piece: int):
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
    

    if captured_piece == b.WR:
        if to_sq == 0: b.CASTLING_WQ = False
        if to_sq == 7: b.CASTLING_WK = False
    elif captured_piece == b.BR:
        if to_sq == 56: b.CASTLING_BQ = False
        if to_sq == 63: b.CASTLING_BK = False



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



def castling_condition_Queen_side(square_num) ->bool:
    num = b.SQUARE_MAP[square_num]
    
    if num == b.WK:  
        if not b.CASTLING_WQ: return False
        if b.ALL_OCCUPANCY & b.WHITE_QUEENSIDE_EMPTY: return False
        if th.Threats.square_attacked_by_black(4): return False  
        if th.Threats.square_attacked_by_black(3): return False  
        if th.Threats.square_attacked_by_black(2): return False  
        
        return True

    elif num == b.BK:  # Black
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
            # King e1 → g1
            bo.Board.Normal_attack(4, 6, b.WK, 1<<4, 1<<6, b.E)
            # Rook h1 → f1
            bo.Board.Normal_attack(7, 5, b.WR, 1<<7, 1<<5, b.E)
        else:
            # King e1 → c1
            bo.Board.Normal_attack(4, 2, b.WK, 1<<4, 1<<2, b.E)
            # Rook a1 → d1
            bo.Board.Normal_attack(0, 3, b.WR, 1<<0, 1<<3, b.E)

    else:  # Black
        if kingside:
            # King e8 → g8
            bo.Board.Normal_attack(60, 62, b.BK, 1<<60, 1<<62, b.E)
            # Rook h8 → f8
            bo.Board.Normal_attack(63, 61, b.BR, 1<<63, 1<<61, b.E)
        else:
            # King e8 → c8
            bo.Board.Normal_attack(60, 58, b.BK, 1<<60, 1<<58, b.E)
            # Rook a8 → d8
            bo.Board.Normal_attack(56, 59, b.BR, 1<<56, 1<<59, b.E)


def Restore_castling(moved_piece: int, to_sq: int):
    if moved_piece == b.WK and to_sq == 6:  # White kingside
        bo.Board.Normal_undo(b.WK, 4, 6, 1<<6, 1<<4, b.E)
        bo.Board.Normal_undo(b.WR, 7, 5, 1<<5, 1<<7, b.E)

    elif moved_piece == b.WK and to_sq == 2:  # White queenside
        bo.Board.Normal_undo(b.WK, 4, 2, 1<<2, 1<<4, b.E)
        bo.Board.Normal_undo(b.WR, 0, 3, 1<<3, 1<<0, b.E)

    elif moved_piece == b.BK and to_sq == 62:  # Black kingside
        bo.Board.Normal_undo(b.BK, 60, 62, 1<<62, 1<<60, b.E)
        bo.Board.Normal_undo(b.BR, 63, 61, 1<<61, 1<<63, b.E)

    elif moved_piece == b.BK and to_sq == 58:  # Black queenside
        bo.Board.Normal_undo(b.BK, 60, 58, 1<<58, 1<<60, b.E)
        bo.Board.Normal_undo(b.BR, 56, 59, 1<<59, 1<<56, b.E)



def castling_trigger(from_sq: int,to_sq: int,moved_piece: int):
    if moved_piece == b.WK and from_sq == 4 and to_sq == 6:
        Execute_castling(0, kingside=True)
    elif moved_piece == b.WK and from_sq == 4 and to_sq == 2:
        Execute_castling(0, kingside=False)
    elif moved_piece == b.BK and from_sq == 60 and to_sq == 62:
        Execute_castling(1, kingside=True)
    elif moved_piece == b.BK and from_sq == 60 and to_sq == 58:
        Execute_castling(1, kingside=False)

def Castling_execute(moved_piece, flags, to_sq):
    if moved_piece == b.WK:
        ca.Execute_castling(0, kingside=(to_sq == 6))  # g1
        if to_sq == 2:                                # c1
            ca.Execute_castling(0, kingside=False)
    elif moved_piece == b.BK:
        if to_sq == 62:                               # g8
            ca.Execute_castling(1, kingside=True)
        elif to_sq == 58:                             # c8
            ca.Execute_castling(1, kingside=False)


