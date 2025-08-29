from board import *
from _init_ import * 
from utils import * 
from moves import *
from threats import *
import bitboard as b
import magic as m



Board.Fresh_reset()
Board.Update_occupancy()
# check = Threats.Return_threat_map()
# print(check)
      


while True:#========================Pick_side==================
    side = input("Choose side:")
    side = Side_pick(side)
    if side is False:
        print("use format w/o")
        continue
    print(side,"Turn")            
    break
    
while True:#========================Game_loop==================
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
    if Board.piece_exists(to_sq,b.ALL_OCCUPANCY) is False:
        Action = Piece_move(from_sq)
    else:
        Action = Piece_attack(from_sq)
    if not Valid_attack(Action, to_sq):
        print("Invalid move")
        continue
#=========================CHECK IF FIRENDLY========================
    Friendly = Check_for_friendly_target(from_sq,to_sq)
    if Friendly is False:
        print("Target square is friendly")
        continue
#========================= Change side ========================
    side = Side_change(side)
    print(side,"Turn")            







#=========================wUPDATE THE PIECES LISTS==================
    Board.Move_attacker(from_sq, to_sq)
    Board.Update_occupancy()
    print(b.ALL_OCCUPANCY,"check1111111")
    # check = Threats.Return_threat_map()
    # print(check)

    

#in magic file turn off (MAGIC_NUMBER_BISHOP = [0]*64) and (MAGIC_NUMBER_ROOK = [0]*64)
#it reset the list with magic numbers.
#after turn off the index of rook is incorect. 
#1.check if the generated number is correct 


    


    
    
