from bitboard import *

"""Creating all the walkable squares from each square for every piece """
init_Knight_mask()
init_Pawn_mask()
init_King_mask()
init_Rook_mask()
init_Bishop_mask()
init_Queen_mask()

"""Same as piece mask but without the edges"""
init_Rook_exclude_edges()
init_Bishop_exclude_edges()


"""Creating all the possible subset from each square for sliding pieces"""
init_Rook_blocker_subset_build()
init_Bishop_blocker_subset_build()

"""Creating all the possible attack bitboard from each square for sliding pieces based on blocker subset"""
init_Rook_attack()
init_Bishop_attack()