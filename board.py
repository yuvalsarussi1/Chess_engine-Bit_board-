import bitboard as b
import threats as th
import utils as u
import moves as mo
import move_record as mr
import castling as ca
import en_passant as en
import promotion as pro

class Board:
    def __init__(self):
        self.reset()

#=====================START BOARD AND PIECES DEF=====================
    @staticmethod
    def Fresh_reset():
        for square_1 in range(8):
            #PIECE_DICT --> (P:1 << 8)
            b.PIECE_DICT[b.WP] |= (1 << (8 + square_1))
            b.PIECE_DICT[b.BP] |= (1 << (48 + square_1))
            b.PIECE_DICT[b.WHITE_ROW1_PIECES[square_1]] |= (1 << square_1) 
            b.PIECE_DICT[b.BLACK_ROW1_PIECES[square_1]] |= (1 << (56 + square_1)) 
    @staticmethod
    def Update_occupancy():
        #Creat the occupancy or update it
        global WHITE_OCCUPANCY,BLACK_OCCUPANCY,ALL_OCCUPANCY,PIECE_DICT
        b.WHITE_OCCUPANCY =  (b.PIECE_DICT[b.WP] | b.PIECE_DICT[b.WN] | b.PIECE_DICT[b.WB]|
                            b.PIECE_DICT[b.WR] | b.PIECE_DICT[b.WQ] | b.PIECE_DICT[b.WK])
        b.BLACK_OCCUPANCY =  (b.PIECE_DICT[b.BP] | b.PIECE_DICT[b.BN] | b.PIECE_DICT[b.BB]|
                            b.PIECE_DICT[b.BR] | b.PIECE_DICT[b.BQ] | b.PIECE_DICT[b.BK])
        b.ALL_OCCUPANCY   = b.BLACK_OCCUPANCY | b.WHITE_OCCUPANCY
        


    def piece_exists(square_num: int, occupancy: int) -> bool:
        """Check if a piece exists at the given bit index in the occupancy bitboard."""
        return (occupancy & (1 << square_num)) != 0
    
    def print_board_list(lst, top_down=True):
        rows = [lst[i:i+8] for i in range(0, len(lst), 8)]
        if top_down:
            rows = rows[::-1]

        # Column labels
        col_labels = "  " + " ".join("abcdefgh")
        print(" ",col_labels)
        print(" +-----------------+")

        for i, row in enumerate(rows):
            # Row numbers (8 down to 1 if top_down is True)
            row_num = 8 - i if top_down else i + 1
            row_str = " ".join(b.PIECE_TO_CHAR[p] for p in row)
            print(f"{row_num} | {row_str} | {row_num}")
        print(" +-----------------+")
        print(" ",col_labels)


#=====================CHECK DEF=====================
    def in_check_white(king_sq: int) -> bool:
        if b.PAWN_MASK_EAT_BLACK[king_sq] & b.PIECE_DICT[b.BP]: return True
        if b.KNIGHT_MASK[king_sq]        & b.PIECE_DICT[b.BN]: return True
        if mo.Bishop_attack(king_sq)     & (b.PIECE_DICT[b.BB] | b.PIECE_DICT[b.BQ]): return True
        if mo.Rook_attack(king_sq)       & (b.PIECE_DICT[b.BR] | b.PIECE_DICT[b.BQ]): return True
        if b.KING_MASK[king_sq]          & b.PIECE_DICT[b.BK]: return True
        return False

    def in_check_black(king_sq: int) -> bool:
        if b.PAWN_MASK_EAT_WHITE[king_sq] & b.PIECE_DICT[b.WP]: return True
        if b.KNIGHT_MASK[king_sq]         & b.PIECE_DICT[b.WN]: return True
        if mo.Bishop_attack(king_sq)      & (b.PIECE_DICT[b.WB] | b.PIECE_DICT[b.WQ]): return True
        if mo.Rook_attack(king_sq)        & (b.PIECE_DICT[b.WR] | b.PIECE_DICT[b.WQ]): return True
        if b.KING_MASK[king_sq]           & b.PIECE_DICT[b.WK]: return True
        return False

    def Check_state(side: int) -> bool:
        return Board.in_check_white(b.WHITE_KING_SQ) if side == 0 else Board.in_check_black(b.BLACK_KING_SQ)



    def Normal_attack(from_sq,to_sq,moved_piece,from_mask,to_mask,captured_piece):
        
        if moved_piece == b.WK:
            b.WHITE_KING_SQ = to_sq
        elif moved_piece == b.BK:
            b.BLACK_KING_SQ = to_sq

        # --- update bitboards ---
        b.PIECE_DICT[moved_piece] &= ~from_mask
        b.PIECE_DICT[moved_piece] |= to_mask
        if captured_piece != b.E:
            b.PIECE_DICT[captured_piece] &= ~to_mask

        # --- update square map ---
        b.SQUARE_MAP[to_sq]   = moved_piece
        b.SQUARE_MAP[from_sq] = b.E

        # --- update occupancies incrementally ---
        b.ALL_OCCUPANCY ^= from_mask
        b.ALL_OCCUPANCY |= to_mask

        # --- update color occupancies incrementally ---
        if moved_piece <= b.WK:  # white moved
            b.WHITE_OCCUPANCY ^= from_mask
            b.WHITE_OCCUPANCY |= to_mask
        else:                    # black moved
            b.BLACK_OCCUPANCY ^= from_mask
            b.BLACK_OCCUPANCY |= to_mask
        # --- update color occupancies for captured piece ---
        if captured_piece != b.E:
            if captured_piece <= b.WK:
                b.WHITE_OCCUPANCY ^= to_mask
            else:
                b.BLACK_OCCUPANCY ^= to_mask

    def Normal_undo(moved_piece,from_sq,to_sq,to_mask,from_mask,captured_piece):
        if moved_piece == b.WK:
            b.WHITE_KING_SQ = from_sq
        elif moved_piece == b.BK:
            b.BLACK_KING_SQ = from_sq


        # --- restore moved piece ---
        b.PIECE_DICT[moved_piece] &= ~to_mask
        b.PIECE_DICT[moved_piece] |= from_mask
        b.SQUARE_MAP[from_sq] = moved_piece

        # --- restore captured piece ---
        if captured_piece != b.E:
            b.PIECE_DICT[captured_piece] |= to_mask
            b.SQUARE_MAP[to_sq] = captured_piece
        else:
            b.SQUARE_MAP[to_sq] = b.E

        # --- restore occupancies ---
        b.ALL_OCCUPANCY ^= to_mask
        b.ALL_OCCUPANCY |= from_mask

        if moved_piece <= b.WK:
            b.WHITE_OCCUPANCY ^= to_mask
            b.WHITE_OCCUPANCY |= from_mask
        else:
            b.BLACK_OCCUPANCY ^= to_mask
            b.BLACK_OCCUPANCY |= from_mask

        if captured_piece != b.E:
            if captured_piece <= b.WK:
                b.WHITE_OCCUPANCY |= to_mask
            else:
                b.BLACK_OCCUPANCY |= to_mask


#=====================MOVE EXECUTE DEF=====================
    def Move_attacker(from_sq: int, to_sq: int, flags = mr.MoveRecord.NONE_FLAG):
        from_mask = 1 << from_sq
        to_mask   = 1 << to_sq
        old_ep = b.EN_PASSANT_SQ
        moved_piece = b.SQUARE_MAP[from_sq]
        captured_piece = b.SQUARE_MAP[to_sq]

        # --- special flags ---
        if moved_piece == b.WK and from_sq == 4 and to_sq in (6, 2):
            flags = mr.MoveRecord.CASTLE_FLAG
        elif moved_piece == b.BK and from_sq == 60 and to_sq in (62, 58):
            flags = mr.MoveRecord.CASTLE_FLAG
        elif moved_piece == b.WP and to_sq == b.EN_PASSANT_SQ and captured_piece == b.E:
            flags = mr.MoveRecord.EN_PASSANT_FLAG
        elif moved_piece == b.BP and to_sq == b.EN_PASSANT_SQ and captured_piece == b.E:
            flags = mr.MoveRecord.EN_PASSANT_FLAG
        
        elif moved_piece == b.WP and to_sq >= 56:
            flags = mr.MoveRecord.PROMOTION_FLAG
        elif moved_piece == b.BP and to_sq <= 7:
            flags = mr.MoveRecord.PROMOTION_FLAG
        
        else:
            flags = mr.MoveRecord.NONE_FLAG
            Board.Normal_attack(from_sq,to_sq,moved_piece,from_mask,to_mask,captured_piece)

        
        if flags == mr.MoveRecord.CASTLE_FLAG:
            ca.Castling_execute(moved_piece,flags,to_sq)
        
        en.Update_en_square(moved_piece,from_sq,to_sq)
        if flags == mr.MoveRecord.EN_PASSANT_FLAG:
            en.En_passant_execute(moved_piece, flags,from_sq,to_sq)
        if flags == mr.MoveRecord.PROMOTION_FLAG:
            print(b.PROMOTION_PIECE,"before execute")
            pro.promotion_execute(from_sq,to_sq,from_mask,to_mask,moved_piece,b.PROMOTION_PIECE,flags,captured_piece)
        
        
        
        
        
        
        
        # --- record of moves ---
        Move_record = mr.MoveRecord(from_sq, to_sq, moved_piece, captured_piece, old_ep ,b.PROMOTION_PIECE,flags)
        b.MOVE_HISTORY.append(Move_record)
        
        return moved_piece, captured_piece

    def Undo_move():
        record = b.MOVE_HISTORY.pop()
        from_sq, to_sq = record.from_sq, record.to_sq
        moved_piece, captured_piece = record.moved_piece, record.captured_piece
        flags = record.flags
        b.EN_PASSANT_SQ =  record.en_sq
        from_mask = 1 << from_sq
        to_mask   = 1 << to_sq

        
        print(flags,"flags check")
        if flags == mr.MoveRecord.CASTLE_FLAG:
            ca.Restore_castling(moved_piece, to_sq)
            return 
        elif flags == mr.MoveRecord.EN_PASSANT_FLAG:
            if moved_piece == b.WP:
                en.en_passant_undo(from_sq, to_sq, 0)  # White undo
            else:  # b.BP
                en.en_passant_undo(from_sq, to_sq, 1)  # Black undo
            return
        elif flags == mr.MoveRecord.PROMOTION_FLAG:
            pro.promotion_undo(from_sq,to_sq,from_mask,to_mask,moved_piece,flags,record)
            return
        else:
            Board.Normal_undo(moved_piece,from_sq,to_sq,to_mask,from_mask,captured_piece)
            return







