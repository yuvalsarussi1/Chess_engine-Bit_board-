from bitboard import *
from magic import *
#condition_1 = ligal piece move

#==========================================Pieces attack index return=================================================
def Pawn_attacks_eat(square_num: int) -> int:
    return PAWN_MASK_EAT[square_num]
def Pawn_attacks_walk(square_num: int) -> int:
    return PAWN_MASK_WALK[square_num]
def Knight_attacks(square_num: int) -> int:
   return KNIGHT_MASK[square_num]
def King_attack(square_num: int) -> int:
    return KING_MASK[square_num]
def Rook_attack(square_num: int) -> int:
    occ = ALL_OCCUPANCY & ROOK_EXCLUDE_EDGES[square_num]
    row, col = divmod(square_num, 8)
    attack_mask = (occ * MAGIC_NUMBER_ROOK[square_num]) >> (64 - ROOK_RELEVANT_BITS[row][col])
    return ROOK_ATTACKS[square_num][attack_mask]
def Bishop_attack(square_num: int) -> int:
    occ = ALL_OCCUPANCY & BISHOP_EXCLUDE_EDGES[square_num]
    row, col = divmod(square_num, 8)
    attack_mask = (occ * MAGIC_NUMBER_BISHOP[square_num]) >> (64 - BISHOP_RELEVANT_BITS[row][col])
    return BISHOP_ATTACKS[square_num][attack_mask]
def Queen_attack(square_num: int) -> int:
    return Rook_attack(square_num) | Bishop_attack(square_num)
#===========================================================================================


