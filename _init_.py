# import magic as m
import bitboard as b
import magic as m
import random
"""Creating all the walkable squares from each square for every piece """
b.init_Knight_mask()
b.init_Pawn_mask()
b.init_King_mask() 
b.init_Rook_mask()
b.init_Bishop_mask()
b.init_Queen_mask()

"""Same as piece mask but without the edges"""
b.init_Rook_exclude_edges()
b.init_Bishop_exclude_edges()


"""Creating all the possible subset from each square for sliding pieces"""
b.init_Rook_blocker_subset_build()
b.init_Bishop_blocker_subset_build()

"""Creating all the possible attack bitboard from each square for sliding pieces based on blocker subset"""
b.init_Rook_attack_no_magic()
b.init_Bishop_attack_no_magic()

"""Init relevant bits for magic bitboard"""
m.init_rook_relevant_bits()
m.init_bishop_relevant_bits()

"""Creat magic number list for sliding pieces"""
m.Creat_rook_attacks_all_squares()
m.Creat_bishop_attacks_all_squares()




