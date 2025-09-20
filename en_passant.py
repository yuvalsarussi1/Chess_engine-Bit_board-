import bitboard as b
import move_record as mr
import board as bo

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

    moved_piece = b.WP if side == 0 else b.BP
    captured_piece = b.E  # en passant looks empty, Normal_attack handles just the mover

    # First do the normal move
    bo.Board.Normal_attack(from_sq, to_sq, moved_piece, from_mask, to_mask, captured_piece)

    # Now handle the special captured pawn
    if side == 0:  # White capturing black pawn
        captured_sq   = to_sq - 8
        captured_mask = (1 << captured_sq)

        b.PIECE_DICT[b.BP] &= ~captured_mask
        b.SQUARE_MAP[captured_sq] = b.E
        b.BLACK_OCCUPANCY &= ~captured_mask
        b.ALL_OCCUPANCY   &= ~captured_mask

    else:  # Black capturing white pawn
        captured_sq   = to_sq + 8
        captured_mask = (1 << captured_sq)

        b.PIECE_DICT[b.WP] &= ~captured_mask
        b.SQUARE_MAP[captured_sq] = b.E
        b.WHITE_OCCUPANCY &= ~captured_mask
        b.ALL_OCCUPANCY   &= ~captured_mask



# undo
def en_passant_undo(from_sq, to_sq, side):
    from_mask = 1 << from_sq
    to_mask   = 1 << to_sq
    moved_piece = b.WP if side == 0 else b.BP
    captured_piece = b.BP if side == 0 else b.WP

    # normal undo first
    bo.Board.Normal_undo(moved_piece, from_sq, to_sq, to_mask, from_mask, b.E)

    # restore the hidden captured pawn
    captured_sq   = to_sq - 8 if side == 0 else to_sq + 8
    captured_mask = 1 << captured_sq
    b.PIECE_DICT[captured_piece] |= captured_mask
    b.SQUARE_MAP[captured_sq] = captured_piece
    if side == 0:
        b.BLACK_OCCUPANCY |= captured_mask
    else:
        b.WHITE_OCCUPANCY |= captured_mask
    b.ALL_OCCUPANCY |= captured_mask



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