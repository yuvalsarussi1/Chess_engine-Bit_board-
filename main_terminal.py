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
    print(side,"Turn")            
    break
    
while True:#========================Game_oop==================
    Board.print_board_list(b.SQUARE_MAP,True)
    Update_PIECES_TURN(side)
#=========================ENTER PIECE SQUARE COORD=================
    from_sq = input ("Choose piece:")
    from_sq = coord_converter_num(from_sq)
    if from_sq is False:
        print("Invalid Input")
        continue
#=========================CHECK IF THE COORD ARE VALID=============
    Valid = Valid_piece(from_sq,side)
    if Valid is False:
        print("Error move")
        continue
#=========================ENTER CAPTURE SQUARE COORD===============
    to_sq = input ("Choose square:")
    to_sq = coord_converter_num(to_sq)
    if to_sq is False:
        print("Invalid Input")
        continue
#=================PICK PIECE AND CHECK FOR VALID MOVE==============
    Attacks = Piece_select(from_sq)
    Attacks = Valid_attack(Attacks,to_sq)
    if Attacks is False:
        print("Invalid move")
        continue
#=========================CHECK IF FIRENDLY========================
    Friendly = Check_for_friendly_target(from_sq,to_sq)
    if Friendly is False:
        print("Target square is friendly")
        continue
    

#=========================UPDATE THE PIECES LISTS==================
    Board.Move_attacker(from_sq, to_sq)
    Board.Update_occupancy()

    side = Side_change(side)
    print(side,"Turn")            


    


    


    


    
    
