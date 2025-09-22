from board import *
from _init_ import * 
from utils import * 
from moves import *
import bitboard as b
import legal_moves as ch
import castling as ca
import move_generate as mog
import fen as fe
import search_engine as se

#=== explanation for player_vs_engine.py ===
# This script facilitates a chess game between a human player and a chess engine.
# It allows the player to choose their side (white or black) and enter moves in standard chess notation.
# The engine uses a search algorithm to determine its moves. The game continues until a checkmate, stalemate, or draw condition is met.
# The script also supports initializing the game from a FEN string for custom starting positions.


## The main components of the script include:
# - Side selection: The player can choose to play as white or black.
# - Move input and validation: The player inputs their moves, which are validated for legality.
# - Engine move generation: The engine calculates its moves using a search algorithm.
# - Game state management: The script keeps track of the board state, checks for check/checkmate/stalemate, and updates the board after each move.
# - Endgame conditions: The game ends when a player is checkmated, stalemated, or a draw condition is met.


def Player_move(side):
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
        #=========================MAKE PROMOTION=============================
        if moved_piece in (1,7) and not (7 < to_sq < 56):
            Promotion_select(side)
        #=========================EXECUTE THE MOVE==================
        Board.Move_attacker(from_sq, to_sq)
        #========================= Check for self check ========================
        if Board.Check_state(side):  
            print("Illegal move! You cannot leave your king in check.")
            Board.Undo_move()
            continue   
        #================= UPDATE PIECE MOVED ========================
        ca.Piece_moved(from_sq,to_sq,moved_piece,captured_piece) # update castling rights
        #========================= SIDE CHANGE ========================
        side = Side_change(side)
        Update_PIECES_TURN(side)
        #========================= CHECKMATE ========================
        if Board.Check_state(side):
            print(f"{'White' if side == 'w' else 'Black'} is in check")
            
            mog.All_Move_generate()
            has_move = ch.Has_legal_move(side)
            
            if not has_move:
                print(f"Checkmate! {'White' if side == 1 else 'Black'} wins!") 
                break
            else:
                print("check but not mate")
                
        else:
            mog.All_Move_generate()
            has_move = ch.Has_legal_move(side)
            if has_move == False:
                print("Stalemate! Game drawn.")
                break
        return side,moved_piece,captured_piece
        
#========================= GAME LOOP =========================
while True:
    Fen_choice = int(input("FEN? 1/0:"))
    if Fen_choice == 1:
        side = fe.Fen.FEN_Option("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    else:
        Board.Fresh_reset()
        #========================Pick_side==================
        while True:
            side = int(input("Choose side:"))
            side = Side_pick(side)
            if side is False:
                print("use format w/o")
                continue
            print("White Turn") if side == 0 else print("Black Turn")                
            break
    Board.Update_occupancy()
    b.ENGINE_SIDE = 1 - side
    while True:
        #========================= ENGINE PLAY ==================
        if side == b.ENGINE_SIDE:
            se.Search_engine_eval(4,side)
            print("Engine played")
            side = Side_change(side)

        
        #=========================PLAYER PLAY ==================
        side,moved_piece,captured_piece = Player_move(side)

        print("White Turn") if side == 0 else print("Black Turn")   

        #=========================END GAME CONDITION=======================
        if b.WHITE_OCCUPANCY == 0 or b.BLACK_OCCUPANCY == 0 :
            print("Game over")
        b.ALL_OCCUPANCY = b.WHITE_OCCUPANCY | b.BLACK_OCCUPANCY

        half_moves = Move_counter(moved_piece,captured_piece,side)
        if half_moves == 75:
            break
        


