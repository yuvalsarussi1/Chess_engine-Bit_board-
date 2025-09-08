from board import *
import bitboard as b
import moves as mo
def Coord_converter_index(coord: str) -> int: #change to enter both piece and target in one input
    if len(coord) == 2:
        file = ord(coord[0].lower()) - ord("a")
        if (0 <= file <= 7) and (coord[1].isdigit()):   
            rank = int(coord[1]) - 1                  
            if (0 <= rank <= 7):
                index = rank * 8 + file                    
                return 1 << index
            return False      
        return False
    return False

def coord_converter_num(coord: str) -> int:
    index = 0
    if len(coord) == 2:
        file = ord(coord[0].lower()) - ord("a")
        if (0 <= file <= 7) and (coord[1].isdigit()):   
            rank = int(coord[1]) - 1                  
            if (0 <= rank <= 7):
                    index = (rank*8) + (file)
                    return index
            return False       
        return False 
    return False

def Check_for_friendly_target(square_num: int,target: int) -> bool:
    square_index = (1 << square_num)
    target_index = (1 << target)
     
    if (square_index & b.WHITE_OCCUPANCY) and (target_index & b.WHITE_OCCUPANCY):
          return False
     
    if (square_index & b.BLACK_OCCUPANCY) and (target_index & b.BLACK_OCCUPANCY):
          return False
     
    return True


def Update_PIECES_TURN(side: bool):
    global PIECES_TURN
    if side == 0:
          b.PIECES_TURN = [b.WP,b.WR,b.WN,b.WB,b.WQ,b.WK]
    
    if side == 1:
          b.PIECES_TURN = [b.BP, b.BR, b.BN, b.BB, b.BQ, b.BK]
    
def Valid_piece(square_num: int,side) -> bool:
     square_index = (1 << square_num)
    #  print("check", b.WHITE_OCCUPANCY)
     if side == 0 and square_index & b.WHITE_OCCUPANCY:
          return True
     if side == 1 and square_index & b.BLACK_OCCUPANCY:
          return True
     else:    
        return False
    
def Side_pick(side):
     if side == 0:
          return 0
     if side == 1:
          return 1
     else:
          return False
     
def Side_change(side):
    if side == 0:
        new_side = 1
    if side == 1:
        new_side = 0
    return new_side

def Score_change(to_sq: int,side: bool):#not working with en_passant 
    piece = b.SQUARE_MAP[to_sq]
    if side == 0:
          b.WHITE_SCORE += b.PIECE_SCORES[piece]
    if side == 1:
          b.BLACK_SCORE += b.PIECE_SCORES[piece]

def attacks_of_piece(piece, square):
    return mo.PIECE_ATTACKS[piece](square)