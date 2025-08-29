from board import *
from _init_ import * 
from utils import * 
from moves import *
import threats as th
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
    
    Board.Check_state(side)
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





#=========================Assain pieces========================
    moved_piece = b.SQUARE_MAP[from_sq]#can be str(piece_name)
    captured_piece = b.SQUARE_MAP[to_sq]#can be str(piece_name) or str(".")

#=========================UPDATE THE PIECES LISTS==================
    Board.Move_attacker(from_sq, to_sq)
    Board.Update_occupancy()
    th.Threats.get_threat_map()
    

    

#========================= Undo move ========================    
    if Board.Check_state(side):
        Board.Undo_move(from_sq,to_sq,moved_piece,captured_piece,side)
        print("Move undone (illegal)")
        continue
#========================= Change side ========================
    side = Side_change(side)
    print(side,"Turn")            
#=========================END GAME CONDITION=======================
    if b.WHITE_OCCUPANCY == 0 or b.BLACK_OCCUPANCY == 0:
        print("Game over")
        break




    
    
