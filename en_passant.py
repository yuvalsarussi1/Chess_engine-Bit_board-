import bitboard as b
import board as bo

# === explanation for en_passant.py ===
# This module handles the en passant rule in chess, which allows a pawn to capture an opponent's
# pawn that has just moved two squares forward from its starting position.
# The module includes functions to determine if an en passant move is possible, execute the move,
# and undo the move if necessary. It also updates the en passant square after each move.
# The functions interact with the board state, including piece positions and occupancy bitboards.




#==========================================En Passant Functions=================================================

# Check if en passant condition is met and return the en passant square if true
def En_passant_condition(from_sq: int, to_sq: int, moved_piece: int) -> int:
    if moved_piece == b.WP:
        if 8 <= from_sq <= 15 and 24 <= to_sq <= 31:
            return (from_sq + to_sq) // 2
    elif moved_piece == b.BP:
        if 48 <= from_sq <= 55 and 32 <= to_sq <= 39:
            return (from_sq + to_sq) // 2
    return -1

# Assign the en passant square in the bitboard module
def Assign_en_passant_sq(en_passant_sq: int):
    if en_passant_sq != -1:
        b.EN_PASSANT_SQ = en_passant_sq

    else:
        b.EN_PASSANT_SQ = -1        

# Execute the en passant move
def En_passant_execute(moved_piece: int, from_sq: int, to_sq: int):
    """Execute en passant capture for a given pawn move."""
    from_mask = 1 << from_sq
    to_mask   = 1 << to_sq

    side = 0 if moved_piece == b.WP else 1
    captured_piece = b.BP if side == 0 else b.WP

    # Do the normal pawn move (destination square looks empty)
    bo.Board.Normal_attack(from_sq, to_sq, moved_piece, from_mask, to_mask, b.E)

    # Remove the pawn that was actually captured
    captured_sq   = to_sq - 8 if side == 0 else to_sq + 8
    captured_mask = 1 << captured_sq

    b.PIECE_DICT[captured_piece] &= ~captured_mask
    b.SQUARE_MAP[captured_sq] = b.E

    if side == 0:  # White captured black
        b.BLACK_OCCUPANCY &= ~captured_mask
    else:          # Black captured white
        b.WHITE_OCCUPANCY &= ~captured_mask

    b.ALL_OCCUPANCY &= ~captured_mask

# Undo the en passant move
def En_passant_undo(from_sq, to_sq, side):
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

# Update the en passant square after a move
def Update_en_square(moved_piece,from_sq,to_sq):
    ep_sq = -1
    if moved_piece == b.WP:
        ep_sq = En_passant_condition(from_sq, to_sq,moved_piece)
    elif moved_piece == b.BP:
        ep_sq = En_passant_condition(from_sq, to_sq,moved_piece)
    Assign_en_passant_sq(ep_sq)