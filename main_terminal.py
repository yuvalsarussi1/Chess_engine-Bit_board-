from board import *
from _init_ import * 
from utils import * 
from moves import *
import bitboard as b



Board.Fresh_reset()
Board.Update_occupancy()
print(hex(b.WHITE_OCCUPANCY))
      



while True:#========================Pick_side==================
    side = input("Choose side:")
    side = Side_pick(side)
    if side is False:
        print("use format w/o")
        continue
    break
    
while True:#========================Game_oop==================
    
    Update_PIECES_TURN(side)

    from_sq = input ("Choose piece:")
    from_sq = coord_converter_num(from_sq)
    if from_sq is False:
        print("Invalid Input")
        continue

    valid = Valid_piece(from_sq,side)
    if valid is False:
        print("Error move")
        continue

    to_sq = input ("Choose square:")
    to_sq = coord_converter_num(to_sq)
    if to_sq is False:
        print("Invalid Input")
        continue

    Attacks = Piece_select(from_sq)
    print(bin(Attacks),"check")
    Attacks = Valid_attack(Attacks,to_sq)
    print(Attacks,"check_2")
    if Attacks is False:
        print("Invalid move")
        continue

    Friendly = Check_for_friendly_target(from_sq,to_sq)
    if Friendly is False:
        print("Target square is friendly")
        continue
            ### problem with rook attack def 

    


    


    


    
    
