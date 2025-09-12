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


def sanity_check(side):
    print("=== SANITY CHECK ===")
    
    # Side to move
    print("Side to move:", "White" if side != 0 else "Black")
    
    # King positions
    print("White King Square:", b.WHITE_KING_SQ)
    print("Black King Square:", b.BLACK_KING_SQ)

    # Occupancy bitboards
    print("All Occupancy:", bin(b.ALL_OCCUPANCY))
    print("White Occupancy:", bin(b.WHITE_OCCUPANCY))
    print("Black Occupancy:", bin(b.BLACK_OCCUPANCY))

    # Piece counts
    for piece, bb in b.PIECE_DICT.items():
        count = bb.bit_count()
        print(f"{piece}: {count} → {bin(bb)}")

    # Square map consistency
    print("Square Map:")
    for rank in range(7, -1, -1):
        row = []
        for file in range(8):
            sq = rank * 8 + file
            row.append(b.SQUARE_MAP[sq])
        print(row)

    # Cross-check occupancies
    white_from_map = 0
    black_from_map = 0
    for sq, piece in enumerate(b.SQUARE_MAP):
        if piece != b.E:
            if piece.isupper():
                white_from_map |= (1 << sq)
            else:
                black_from_map |= (1 << sq)
    
    if white_from_map != b.WHITE_OCCUPANCY:
        print("[ERROR] White occupancy mismatch!")
    if black_from_map != b.BLACK_OCCUPANCY:
        print("[ERROR] Black occupancy mismatch!")

    print("=== END CHECK ===\n")
     
def  Promotion_select(side):
    while True:
        b.PROMOTION_PIECE = input("Choose promotion - (Q,R,N,B)")
        if b.PROMOTION_PIECE in ("Q","R","N","B") and side == 0:
            b.PROMOTION_PIECE = b.PROMOTION_DICT[b.PROMOTION_PIECE]
            print(b.PROMOTION_PIECE)
            break
        elif b.PROMOTION_PIECE in ("q","r","n","b") and side == 1:
            b.PROMOTION_PIECE = b.PROMOTION_DICT[b.PROMOTION_PIECE]
            break
        else:
             continue

          