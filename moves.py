import bitboard as b
import magic as m
#condition_1 = ligal piece move

#==========================================Pieces attack index return=================================================
def Pawn_attacks_eat(square_num: int) -> int:
    return b.PAWN_MASK_EAT[square_num]
def Pawn_attacks_walk(square_num: int) -> int:
    return b.PAWN_MASK_WALK[square_num]
def Knight_attacks(square_num: int) -> int:
   return b.KNIGHT_MASK[square_num]
def King_attack(square_num: int) -> int:
    return b.KING_MASK[square_num]
def Rook_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.ROOK_EXCLUDE_EDGES[square_num]
    row, col = divmod(square_num, 8)
    attack_mask = (occ * m.MAGIC_NUMBER_ROOK[square_num]) >> (64 - m.ROOK_RELEVANT_BITS[row][col])
    return b.ROOK_ATTACKS[square_num][attack_mask]
def Bishop_attack(square_num: int) -> int:
    occ = b.ALL_OCCUPANCY & b.BISHOP_EXCLUDE_EDGES[square_num]
    row, col = divmod(square_num, 8)
    attack_mask = (occ * m.MAGIC_NUMBER_BISHOP[square_num]) >> (64 - m.BISHOP_RELEVANT_BITS[row][col])
    return b.BISHOP_ATTACKS[square_num][attack_mask]
def Queen_attack(square_num: int) -> int:
    return Rook_attack(square_num) | Bishop_attack(square_num)
#===========================================================================================


PIECE_ATTACKS = {
    "P": lambda sq: Pawn_attacks_walk(sq) | Pawn_attacks_eat(sq),
    "N": lambda sq: Knight_attacks(sq),
    "B": lambda sq: Bishop_attack(sq),
    "R": lambda sq: Rook_attack(sq),
    "Q": lambda sq: Queen_attack(sq),
    "K": lambda sq: King_attack(sq),
    "p": lambda sq: Pawn_attacks_walk(sq) | Pawn_attacks_eat(sq),  # black pawn
    "n": lambda sq: Knight_attacks(sq),
    "b": lambda sq: Bishop_attack(sq),
    "r": lambda sq: Rook_attack(sq),
    "q": lambda sq: Queen_attack(sq),
    "k": lambda sq: King_attack(sq),
    ".": lambda sq: 0   # empty square → no attacks
}

def Piece_select(square_num: int):
    piece = b.SQUARE_MAP[square_num]
    print(piece,"check piece")
    return PIECE_ATTACKS[piece](square_num)

def Valid_attack(attacks: int, target):
    target_index = (1 << target)
    if attacks & target_index:
        return True
    else:
        return False
    
a = Piece_select(0)


### problem with rook attack def 