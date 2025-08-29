import bitboard as b
import magic as m


#condition_1 = ligal piece move

#==========================================Pieces attack index return=================================================
def Pawn_attacks_eat_white(square_num: int) -> int:
    return b.PAWN_MASK_EAT_WHITE[square_num]
def Pawn_walk_white(square_num: int) -> int:
    return b.PAWN_MASK_WALK_WHITE[square_num]
def Pawn_double_white(square_num: int) -> int:
    return b.PAWN_MASK_DOUBLE_WHITE[square_num]
def Pawn_attacks_eat_black(square_num: int) -> int:
    return b.PAWN_MASK_EAT_BLACK[square_num]
def Pawn_walk_black(square_num: int) -> int:
    return b.PAWN_MASK_WALK_BLACK[square_num]
def Pawn_double_black(square_num: int) -> int:
    return b.PAWN_MASK_DOUBLE_BLACK[square_num]
def Knight_attacks(square_num: int) -> int:
   return b.KNIGHT_MASK[square_num]
def King_attack(square_num: int) -> int:
    return b.KING_MASK[square_num]


def Rook_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.ROOK_EXCLUDE_EDGES[square_num]
    index = ((occ * m.MAGIC_NUMBER_ROOK_LIST[square_num]) & ((1 << 64) - 1)) >> (64 - m.ROOK_RELEVANT_BITS[square_num])
    return m.MAGIC_ATTACKS_ROOK[square_num][index]


def Bishop_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.BISHOP_MASK[square_num]
    index = ((occ * m.MAGIC_NUMBER_BISHOP_LIST[square_num]) & ((1 << 64) - 1)) >> (64 - m.BISHOP_RELEVANT_BITS[square_num])
    return m.MAGIC_ATTACKS_BISHOP[square_num][index]


def Queen_attack(square_num: int) -> int:
    return Rook_attack(square_num) | Bishop_attack(square_num)
#===========================================================================================


PIECE_ATTACKS = {
    "P": lambda sq: Pawn_attacks_eat_white(sq),
    "N": lambda sq: Knight_attacks(sq),
    "B": lambda sq: Bishop_attack(sq),
    "R": lambda sq: Rook_attack(sq),
    "Q": lambda sq: Queen_attack(sq),
    "K": lambda sq: King_attack(sq),
    "p": lambda sq: Pawn_attacks_eat_black(sq),  # black pawn
    "n": lambda sq: Knight_attacks(sq),
    "b": lambda sq: Bishop_attack(sq),
    "r": lambda sq: Rook_attack(sq),
    "q": lambda sq: Queen_attack(sq),
    "k": lambda sq: King_attack(sq),
    ".": lambda sq: 0   # empty square → no attacks
}
PIECE_MOVES = PIECE_ATTACKS.copy()
PIECE_MOVES["P"] = lambda sq: Pawn_walk_white(sq) | Pawn_double_white(sq)
PIECE_MOVES["p"] = lambda sq: Pawn_walk_black(sq) | Pawn_double_black(sq)

def Piece_move(from_sq: int):
    piece = b.SQUARE_MAP[from_sq]
    return PIECE_MOVES[piece](from_sq)

def Piece_attack(from_sq: int):
    piece = b.SQUARE_MAP[from_sq]
    print(PIECE_ATTACKS[piece](from_sq),"CHECK ATTACKS")
    return PIECE_ATTACKS[piece](from_sq)

def Valid_attack(attacks: int, target):
    target_index = (1 << target)
    if attacks & target_index:
        return True
    else:
        return False
    



