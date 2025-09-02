import bitboard as b
import magic as m
import castling as ca

#condition_1 = ligal piece move

#==========================================Pieces attack index return=================================================
def Pawn_attacks_eat_white(square_num: int) -> int:
    return b.PAWN_MASK_EAT_WHITE[square_num]
def Pawn_walk_white(square_num: int) -> int:
    return b.PAWN_MASK_WALK_WHITE[square_num]
def Pawn_double_white(square_num: int) -> int:
    one_step = b.PAWN_MASK_WALK_WHITE[square_num]
    two_step = b.PAWN_MASK_DOUBLE_WHITE[square_num]
    if one_step and two_step:
        if (one_step & ~b.ALL_OCCUPANCY) and (two_step & ~b.ALL_OCCUPANCY):
            return two_step
    return 0


def Pawn_attacks_eat_black(square_num: int) -> int:
    return b.PAWN_MASK_EAT_BLACK[square_num]
def Pawn_walk_black(square_num: int) -> int:
    return b.PAWN_MASK_WALK_BLACK[square_num]
def Pawn_double_black(square_num: int) -> int:
    one_step = b.PAWN_MASK_WALK_BLACK[square_num]
    two_step = b.PAWN_MASK_DOUBLE_BLACK[square_num]
    if one_step and two_step:
        if (one_step & ~b.ALL_OCCUPANCY) and (two_step & ~b.ALL_OCCUPANCY):
            return two_step
    return 0


def Knight_attacks(square_num: int) -> int:
   return b.KNIGHT_MASK[square_num]

def King_attack_white(square_num: int) -> int:
    if ca.castling_condition_King_side or ca.castling_condition_Queen_side:
        return (b.KING_MASK[square_num] | b.KING_CASTLING_MASK_WHITE)
    else:
        return b.KING_MASK[square_num]


def King_attack_black(square_num: int) -> int:
    if ca.castling_condition_King_side or ca.castling_condition_Queen_side:
        return (b.KING_MASK[square_num] | b.KING_CASTLING_MASK_BLACK)
    else:
        return b.KING_MASK[square_num]






def Rook_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.ROOK_EXCLUDE_EDGES[square_num]
    index = ((occ * m.MAGIC_NUMBER_ROOK_LIST[square_num]) & ((1 << 64) - 1)) >> (64 - m.ROOK_RELEVANT_BITS[square_num])
    return m.MAGIC_ATTACKS_ROOK[square_num][index]


def Bishop_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.BISHOP_EXCLUDE_EDGES[square_num]
    index = ((occ * m.MAGIC_NUMBER_BISHOP_LIST[square_num]) & ((1 << 64) - 1)) >> (64 - m.BISHOP_RELEVANT_BITS[square_num])
    return m.MAGIC_ATTACKS_BISHOP[square_num][index]


def Queen_attack(square_num: int) -> int:
    return Rook_attack(square_num) | Bishop_attack(square_num)
#===========================================================================================

PIECE_ATTACKS = [lambda sq: 0] * 13
PIECE_MOVES   = [lambda sq: 0] * 13

PIECE_ATTACKS[b.WP] = Pawn_attacks_eat_white
PIECE_ATTACKS[b.WN] = Knight_attacks
PIECE_ATTACKS[b.WB] = Bishop_attack
PIECE_ATTACKS[b.WR] = Rook_attack
PIECE_ATTACKS[b.WQ] = Queen_attack
PIECE_ATTACKS[b.WK] = King_attack_white
PIECE_ATTACKS[b.BP] = Pawn_attacks_eat_black
PIECE_ATTACKS[b.BN] = Knight_attacks
PIECE_ATTACKS[b.BB] = Bishop_attack
PIECE_ATTACKS[b.BR] = Rook_attack
PIECE_ATTACKS[b.BQ] = Queen_attack
PIECE_ATTACKS[b.BK] = King_attack_black

# White pieces
PIECE_MOVES[b.WP] = lambda sq: (
    (Pawn_walk_white(sq) & ~b.ALL_OCCUPANCY) |
    (Pawn_double_white(sq) & ~b.ALL_OCCUPANCY) |
    (Pawn_attacks_eat_white(sq) & b.BLACK_OCCUPANCY)
)
PIECE_MOVES[b.WN] = lambda sq: Knight_attacks(sq) & ~b.WHITE_OCCUPANCY
PIECE_MOVES[b.WB] = lambda sq: Bishop_attack(sq) & ~b.WHITE_OCCUPANCY
PIECE_MOVES[b.WR] = lambda sq: Rook_attack(sq)   & ~b.WHITE_OCCUPANCY
PIECE_MOVES[b.WQ] = lambda sq: Queen_attack(sq)  & ~b.WHITE_OCCUPANCY
PIECE_MOVES[b.WK] = lambda sq: King_attack_white(sq)   & ~b.WHITE_OCCUPANCY

# Black pieces
PIECE_MOVES[b.BP] = lambda sq: (
    (Pawn_walk_black(sq) & ~b.ALL_OCCUPANCY) |
    (Pawn_double_black(sq) & ~b.ALL_OCCUPANCY) |
    (Pawn_attacks_eat_black(sq) & b.WHITE_OCCUPANCY)
)
PIECE_MOVES[b.BN] = lambda sq: Knight_attacks(sq) & ~b.BLACK_OCCUPANCY
PIECE_MOVES[b.BB] = lambda sq: Bishop_attack(sq) & ~b.BLACK_OCCUPANCY
PIECE_MOVES[b.BR] = lambda sq: Rook_attack(sq)   & ~b.BLACK_OCCUPANCY
PIECE_MOVES[b.BQ] = lambda sq: Queen_attack(sq)  & ~b.BLACK_OCCUPANCY
PIECE_MOVES[b.BK] = lambda sq: King_attack_black(sq)   & ~b.BLACK_OCCUPANCY




def Piece_move(from_sq: int):
    piece = b.SQUARE_MAP[from_sq]
    return PIECE_MOVES[piece](from_sq)

def Piece_attack(from_sq: int):
    piece = b.SQUARE_MAP[from_sq]
    # print(PIECE_ATTACKS[piece](from_sq),"CHECK ATTACKS")
    return PIECE_ATTACKS[piece](from_sq)

def Valid_attack(attacks: int, target):
    target_index = (1 << target)
    if attacks & target_index:
        return True
    else:
        return False
    




