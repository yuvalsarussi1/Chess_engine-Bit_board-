from board import *
from _init_ import * 
from utils import * 
from moves import *
import threats as th
import bitboard as b
import magic as m
import checkmate as ch
import time
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
    from_sq = coord_converter_num(from_sq) # =square_index not bit 
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
    to_sq = coord_converter_num(to_sq) #=square_index not bit 
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
    th.Threats.threat_map_update()
    

    

#========================= Check for self check ========================    
    if Board.Check_state(side):  
        print("Illegal move! You cannot leave your king in check.")
        Board.Undo_move(from_sq, to_sq, moved_piece, captured_piece)
        continue   # ask player for another move


#========================= Change side ========================
    side = Side_change(side)
#========================= Check for checkmate ========================


    if Board.Check_state(side):
        print(f"{'White' if side == 'w' else 'Black'} is in check")
        ch.All_Move_generate()

        All_legal_moves = ch.Has_legal_move(side)
        if All_legal_moves == 0:
            print("checkmate!")
            break

        else:
            print("check but not mate")
            print("Legal moves:", All_legal_moves)
            continue
    else:
        
        ch.All_Move_generate()
        All_legal_moves = ch.Has_legal_move(side)
        if All_legal_moves == 0:
            print("stalemate!")
            break
            
        
        

#================================================
    print(side,"Turn11")            
#=========================END GAME CONDITION=======================
    if b.WHITE_OCCUPANCY == 0 or b.BLACK_OCCUPANCY == 0:
        print("Game over")
        break



    start = time.perf_counter()
    N = 1000
    for _ in range(N):
        ch.All_Move_generate()
        ch.Has_legal_move('w')  # or 'b'
    end = time.perf_counter()
    print(f"{N / (end-start):,.0f} positions/sec")


    
    
