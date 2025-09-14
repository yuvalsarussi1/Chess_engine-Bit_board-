from board import *
from _init_ import * 
from utils import * 
from moves import *
import threats as th
import bitboard as b
import magic as m
import legal_moves as ch
import time
import castling as ca
import move_generate as mog
import fen as fe

# fen_obj = fe.Fen.split_fen("rnb1kb1r/pppp1Qpp/5n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
# board = fe.Fen.board_mask(fen_obj)
# fe.Fen.Piece_dict_fen(board)
# fe.Fen.Square_map_fen(board)


check = int(input("FEN? 1/0"))
if check == 1:
    fen_obj = fe.Fen.split_fen("r3k2r/pppqppbp/2np1np1/8/2BPP3/2N2N2/PPP2PPP/R1BQ1RK1 w k - 4 8")
    board = fe.Fen.board_mask(fen_obj)
    side = fe.Fen.side_to_move(fen_obj)
    fe.Fen.castling_fen(fen_obj)
    fe.Fen.en_passant_fen(fen_obj)
    fe.Fen.Piece_dict_fen(board)
    fe.Fen.Square_map_fen(board)
else:
    Board.Fresh_reset()
    #========================Pick_side==================
    while True:
        side = int(input("Choose side:"))
        side = Side_pick(side)
        if side is False:
            print("use format w/o")
            continue
        print(side,"Turn")            
        break
Board.Update_occupancy()


# print(b.PIECE_DICT)
# print(b.SQUARE_MAP)
# print(b.WHITE_OCCUPANCY)
# print(b.BLACK_OCCUPANCY)
# print(side)

#========================Game_loop==================
while True:
    if Board.Check_state(side):
        print("YOU ARE IN CHECK")
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
    Action = Piece_move(from_sq)
    print(Action,"ACTION")
    if not Valid_attack(Action, to_sq):
        print("Invalid move")
        continue
#========================= CHECK IF FIRENDLY========================
    Friendly = Check_for_friendly_target(from_sq,to_sq)
    if Friendly is False:
        print("Target square is friendly")
        continue
#=========================ASSAIN PIECES========================
    moved_piece = b.SQUARE_MAP[from_sq] # int(piece_name)
    captured_piece = b.SQUARE_MAP[to_sq]# int(piece_name)
##=========================PROMOTION ASSIGN========================
    
    print(moved_piece,"moved_piece")

    if moved_piece in (1,7) and not (7 < to_sq < 56):
        Promotion_select(side)
        print(b.PROMOTION_PIECE,"promotion_piece")
    print("check_dest")




   
#=========================UPDATE THE PIECES LISTS==================
    Board.Move_attacker(from_sq, to_sq)
#========================= Check for self check ========================    
    if Board.Check_state(side):  
        print("Illegal move! You cannot leave your king in check.")
        Board.Undo_move()
        continue   # ask player for another move
    ca.Piece_moved(from_sq,moved_piece) # update castling rights

#========================= Change side ========================
    side = Side_change(side)
    Update_PIECES_TURN(side)

#========================= Check for checkmate ===========0=============
    if Board.Check_state(side):
        print(f"{'White' if side == 'w' else 'Black'} is in check")
        mog.All_Move_generate()

        All_legal_moves = ch.Has_legal_move(side)
        if All_legal_moves == False:
            print("checkmate!")
            break
        else:
            print("check but not mate")
            print("Legal moves:", All_legal_moves)
            continue
    else:
        mog.All_Move_generate()
        All_legal_moves = ch.Has_legal_move(side)
        if All_legal_moves == False:
            print("stalemate!")
            break
#================================================
    print(side,"Turn")            
#=========================END GAME CONDITION=======================
    if b.WHITE_OCCUPANCY == 0 or b.BLACK_OCCUPANCY == 0:
        print("Game over")
        break



    start = time.perf_counter()
    N = 1000
    for _ in range(N):
        mog.All_Move_generate()
        ch.All_legal_move(side)  # or 'b'
    end = time.perf_counter()
    print(f"{N / (end-start):,.0f} positions/sec")
    print(b.WHITE_OCCUPANCY,"WHITE")
    print(b.BLACK_OCCUPANCY,"BLACK")
    b.ALL_OCCUPANCY = b.WHITE_OCCUPANCY | b.BLACK_OCCUPANCY