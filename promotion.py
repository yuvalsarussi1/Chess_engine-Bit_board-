import bitboard as b
import move_record as mr
import board as bo

def promotion_execute(from_sq, to_sq, from_mask, to_mask, moved_piece, promotion_piece, captured_piece):
    # First: handle pawn move as a normal attack
    # print("EXEC promotion:", from_sq, to_sq, moved_piece, "->", promotion_piece)
    bo.Board.Normal_attack(from_sq, to_sq, moved_piece, from_mask, to_mask, captured_piece)

    # Now replace pawn with promoted piece
    b.PIECE_DICT[moved_piece] &= ~to_mask   # remove pawn from dest
    b.PIECE_DICT[promotion_piece] |= to_mask
    b.SQUARE_MAP[to_sq] = promotion_piece

    # Update occupancies
    if moved_piece == b.WP:
        b.WHITE_OCCUPANCY &= ~to_mask
        b.WHITE_OCCUPANCY |= to_mask   # redundant but keeps symmetry
    else:
        b.BLACK_OCCUPANCY &= ~to_mask
        b.BLACK_OCCUPANCY |= to_mask





def promotion_undo(from_sq, to_sq, from_mask, to_mask, moved_piece, record):
    
    promoted_piece = record.promotion_piece
    captured_piece = record.captured_piece
    # print("UNDO promotion:", from_sq, to_sq, moved_piece,promoted_piece, "-> restored pawn")
    # Remove promoted piece
    b.PIECE_DICT[promoted_piece] &= ~to_mask
    b.SQUARE_MAP[to_sq] = b.E

    # Restore pawn at from_sq
    b.PIECE_DICT[moved_piece] |= from_mask
    b.SQUARE_MAP[from_sq] = moved_piece

    # Restore occupancies
    if moved_piece == b.WP:
        b.WHITE_OCCUPANCY &= ~to_mask
        b.WHITE_OCCUPANCY |= from_mask
    else:
        b.BLACK_OCCUPANCY &= ~to_mask
        b.BLACK_OCCUPANCY |= from_mask

    # Restore captured piece if any
    if captured_piece != b.E:
        b.PIECE_DICT[captured_piece] |= to_mask
        b.SQUARE_MAP[to_sq] = captured_piece
        if captured_piece <= b.WK:
            b.WHITE_OCCUPANCY |= to_mask
        else:
            b.BLACK_OCCUPANCY |= to_mask

    # Always fix ALL_OCCUPANCY
    b.ALL_OCCUPANCY &= ~to_mask
    b.ALL_OCCUPANCY |= from_mask
    if captured_piece != b.E:
        b.ALL_OCCUPANCY |= to_mask
    

        
