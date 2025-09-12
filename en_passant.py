import bitboard as b
import move_record as mr


def en_passant_condition_1(from_sq: int, to_sq: int, moved_piece: int) -> int:
    if moved_piece == b.WP:
        if 8 <= from_sq <= 15 and 24 <= to_sq <= 31:
            return (from_sq + to_sq) // 2
    elif moved_piece == b.BP:
        if 48 <= from_sq <= 55 and 32 <= to_sq <= 39:
            return (from_sq + to_sq) // 2
    return -1


def assign_en_passant_sq(en_passant_sq: int):
    if en_passant_sq != -1:
        b.EN_PASSANT_SQ = en_passant_sq

    else:
        b.EN_PASSANT_SQ = -1
        

def en_passant_execute(from_sq: int, to_sq: int, side: bool):
    from_mask = (1 << from_sq)
    to_mask   = (1 << to_sq)

    if side == 0:  # White capturing black pawn
        captured_sq   = to_sq - 8   # black pawn is behind the target square
        captured_mask = (1 << captured_sq)

        # Update bitboards
        b.PIECE_DICT[b.WP] &= ~from_mask
        b.PIECE_DICT[b.WP] |= to_mask
        b.PIECE_DICT[b.BP] &= ~captured_mask

        # Update square map
        b.SQUARE_MAP[from_sq] = b.E
        b.SQUARE_MAP[to_sq]   = b.WP
        b.SQUARE_MAP[captured_sq] = b.E

        # Update occupancies
        b.WHITE_OCCUPANCY &= ~from_mask
        b.WHITE_OCCUPANCY |= to_mask
        b.BLACK_OCCUPANCY &= ~captured_mask
        b.ALL_OCCUPANCY   &= ~from_mask
        b.ALL_OCCUPANCY   &= ~captured_mask
        b.ALL_OCCUPANCY   |= to_mask

    else:  # Black capturing white pawn
        captured_sq   = to_sq + 8   # white pawn is behind the target square
        captured_mask = (1 << captured_sq)

        # Update bitboards
        b.PIECE_DICT[b.BP] &= ~from_mask
        b.PIECE_DICT[b.BP] |= to_mask
        b.PIECE_DICT[b.WP] &= ~captured_mask

        # Update square map
        b.SQUARE_MAP[from_sq] = b.E
        b.SQUARE_MAP[to_sq]   = b.BP
        b.SQUARE_MAP[captured_sq] = b.E

        # Update occupancies
        b.BLACK_OCCUPANCY &= ~from_mask
        b.BLACK_OCCUPANCY |= to_mask
        b.WHITE_OCCUPANCY &= ~captured_mask
        b.ALL_OCCUPANCY   &= ~from_mask
        b.ALL_OCCUPANCY   &= ~captured_mask
        b.ALL_OCCUPANCY   |= to_mask


def en_passant_undo(from_sq: int, to_sq: int, side: int):
    from_mask = 1 << from_sq
    to_mask   = 1 << to_sq

    if side == 0:  # White had captured black pawn
        captured_sq   = to_sq - 8
        captured_mask = 1 << captured_sq

        # Restore white pawn
        b.PIECE_DICT[b.WP] &= ~to_mask
        b.PIECE_DICT[b.WP] |= from_mask

        # Restore black pawn
        b.PIECE_DICT[b.BP] |= captured_mask

        # Update square map
        b.SQUARE_MAP[from_sq]     = b.WP
        b.SQUARE_MAP[to_sq]       = b.E
        b.SQUARE_MAP[captured_sq] = b.BP

        # Update occupancies
        b.WHITE_OCCUPANCY &= ~to_mask
        b.WHITE_OCCUPANCY |= from_mask
        b.BLACK_OCCUPANCY |= captured_mask

    else:  # Black had captured white pawn
        captured_sq   = to_sq + 8
        captured_mask = 1 << captured_sq

        # Restore black pawn
        b.PIECE_DICT[b.BP] &= ~to_mask
        b.PIECE_DICT[b.BP] |= from_mask

        # Restore white pawn
        b.PIECE_DICT[b.WP] |= captured_mask

        # Update square map
        b.SQUARE_MAP[from_sq]     = b.BP
        b.SQUARE_MAP[to_sq]       = b.E
        b.SQUARE_MAP[captured_sq] = b.WP

        # Update occupancies
        b.BLACK_OCCUPANCY &= ~to_mask
        b.BLACK_OCCUPANCY |= from_mask
        b.WHITE_OCCUPANCY |= captured_mask


def En_passant_execute(moved_piece,flags,from_sq,to_sq):
    if moved_piece == b.WP:
        en_passant_execute(from_sq,to_sq,0)
    
    else:
        en_passant_execute(from_sq,to_sq,1)


def Update_en_square(moved_piece,from_sq,to_sq):
    ep_sq = -1
    if moved_piece == b.WP:
        ep_sq = en_passant_condition_1(from_sq, to_sq,moved_piece)
    elif moved_piece == b.BP:
        ep_sq = en_passant_condition_1(from_sq, to_sq,moved_piece)
    assign_en_passant_sq(ep_sq)