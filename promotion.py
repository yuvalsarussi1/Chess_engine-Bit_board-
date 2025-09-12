import bitboard as b
import move_record as mr


def promotion_execute(from_sq,to_sq,from_mask,to_mask,moved_piece,promotion_piece,flags,captured_piece):
    # clear pawn
        b.PIECE_DICT[moved_piece] &= ~from_mask

        # if capture → clear captured piece first
        if captured_piece != b.E:
            b.PIECE_DICT[captured_piece] &= ~to_mask
            if captured_piece <= b.WK:
                b.WHITE_OCCUPANCY &= ~to_mask
            else:
                b.BLACK_OCCUPANCY &= ~to_mask

        # place promoted piece
        b.PIECE_DICT[promotion_piece] |= to_mask

        # update square map
        b.SQUARE_MAP[from_sq] = b.E
        b.SQUARE_MAP[to_sq] = promotion_piece

        # update occupancies
        if moved_piece == b.WP:
            b.WHITE_OCCUPANCY &= ~from_mask
            b.WHITE_OCCUPANCY |= to_mask
        else:  # BP
            b.BLACK_OCCUPANCY &= ~from_mask
            b.BLACK_OCCUPANCY |= to_mask




def promotion_undo(from_sq, to_sq, from_mask, to_mask, moved_piece, flags, record):
    if flags == mr.MoveRecord.PROMOTION_FLAG:
        # --- remove promoted piece ---
        
        promoted_piece = record.promotion_piece
        print(promoted_piece,"promoted_piece")
        
        b.PIECE_DICT[promoted_piece] &= ~to_mask
        b.SQUARE_MAP[to_sq] = b.E

        # --- restore pawn ---
        b.PIECE_DICT[moved_piece] |= from_mask
        b.SQUARE_MAP[from_sq] = moved_piece

        # --- restore occupancies ---
        if moved_piece == b.WP:
            b.WHITE_OCCUPANCY &= ~to_mask
            b.WHITE_OCCUPANCY |= from_mask
        else:  # b.BP
            b.BLACK_OCCUPANCY &= ~to_mask
            b.BLACK_OCCUPANCY |= from_mask

        # --- restore captured piece if any ---
        if record.captured_piece != b.E:
            b.PIECE_DICT[record.captured_piece] |= to_mask
            b.SQUARE_MAP[to_sq] = record.captured_piece
            if record.captured_piece <= b.WK:
                b.WHITE_OCCUPANCY |= to_mask
            else:
                b.BLACK_OCCUPANCY |= to_mask

        
