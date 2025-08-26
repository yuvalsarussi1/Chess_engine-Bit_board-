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

    coord = input ("Choose piece:")
    coord = coord_converter_num(coord)
    if coord is False:
        print("Invalid Input")
        continue

    valid = Valid_piece(coord,side)
    if valid is False:
        print("Enemy piece!")
        continue



    


    
    
