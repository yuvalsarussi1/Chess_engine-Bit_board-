from board import *
import bitboard as b

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
    if side == "w":
          b.PIECES_TURN = ["P","R","N","B","Q","K"]
    
    if side == "b":
          b.PIECES_TURN = ["p","r","n","b","q","k"]
    
def Valid_piece(square_num: int,side) -> bool:
     square_index = (1 << square_num)
    #  print("check", b.WHITE_OCCUPANCY)
     if side == "w" and square_index & b.WHITE_OCCUPANCY:
          return True
     if side == "b" and square_index & b.BLACK_OCCUPANCY:
          return True
     else:    
        return False
    

def Side_pick(side):
     if side == "w":
          return "w"
     if side == "b":
          return "b"
     else:
          return False
     
def Side_change(side):
    if side == "w":
        new_side = "b"
    if side == "b":
        new_side = "w"
    return new_side

def Score_change(to_sq: int,side: bool):#not working with en_passant 
    piece = b.SQUARE_MAP[to_sq]
    if side == "w":
          b.WHITE_SCORE += b.PIECE_SCORES[piece]
    if side == "b":
          b.BLACK_SCORE += b.PIECE_SCORES[piece]