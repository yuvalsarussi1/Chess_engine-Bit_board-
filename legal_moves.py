import bitboard as b
import move_generate as mog
from board import *


def iter_bits(mask: int):
    while mask:
        lsb = mask & -mask
        yield lsb.bit_length() - 1   # directly compute index
        mask ^= lsb

def index_to_square(index: int) -> str:
    file = chr((index % 8) + ord('a'))
    rank = str((index // 8) + 1)
    return file + rank




def Count_legal_moves(side):
    legal_moves = 0
    for from_sq,from_mask in mog.MOVES_DICT.items():
        for to_sq in iter_bits(from_mask):
            Board.Move_attacker(from_sq,to_sq)
            if not Board.Check_state(side):
                legal_moves += 1
            Board.Undo_move()

    return legal_moves


# --- if at least 1 move is valid ---
def Has_legal_move(side):
    for from_sq, from_mask in mog.MOVES_DICT.items():
        m = from_mask
        while m:
            lsb = m & -m
            to_sq = lsb.bit_length() - 1
            m ^= lsb
                        
            Board.Move_attacker(from_sq, to_sq)
            if not Board.Check_state(side):
                Board.Undo_move()
                return True
            Board.Undo_move()
    return False

def Promotion_generate(from_sq: int,to_sq: int,side) -> bool:
    promo_list = (b.WQ,b.WR,b.WN,b.WB) if side == 0 else (b.BQ,b.BR,b.BN,b.BB)

    for promotion in promo_list:
        b.PROMOTION_PIECE = promotion
        Board.Move_attacker(from_sq,to_sq)
        if not Board.Check_state(side):
            Board.Undo_move()
            return True
        Board.Undo_move()


# --- debug count all moves ---
def Promotion_generate_debug(from_sq: int,to_sq: int,side) -> int:
    promo_list = (b.WQ,b.WR,b.WN,b.WB) if side == 0 else (b.BQ,b.BR,b.BN,b.BB)

    for promotion in promo_list:
        b.PROMOTION_PIECE = promotion
        Board.Move_attacker(from_sq, to_sq)
        in_check = Board.Check_state(side)
        if not in_check:
            print("   ✅ Legal promotion:", promotion)
        else:
            print("   ❌ Illegal promotion:", promotion)
        Board.Undo_move()

def Has_legal_move_debug(side):
    print("=== DEBUG: Checking all moves for side", side, "===")
    legal_moves = []

    for from_sq, from_mask in mog.MOVES_DICT.items():
        m = from_mask
        while m:
            lsb = m & -m
            to_sq = lsb.bit_length() - 1
            m ^= lsb

            moved_piece = b.SQUARE_MAP[from_sq]

            print(f"Trying move {index_to_square(from_sq)} → {index_to_square(to_sq)} "
                  f"({moved_piece}), side={side}")

            # --- promotion handling ---
            if (moved_piece == b.WP and to_sq > 55 and side == 0) or \
               (moved_piece == b.BP and to_sq < 8 and side == 1):
                Promotion_generate_debug(from_sq, to_sq, side)
                continue  # skip normal execution below
            
            # Execute
            Board.Move_attacker(from_sq, to_sq)

            in_check = Board.Check_state(side)
            if not in_check:
                print("   ✅ Legal move")
                legal_moves.append((from_sq, to_sq, moved_piece))
            else:
                print("   ❌ Illegal move")

            # Undo and continue
            Board.Undo_move()

    print(f"=== DEBUG: Found {len(legal_moves)} legal moves for side {side} ===")
    return legal_moves





# --- list of moves ---
def promotion_append(from_sq: int,to_sq: int,moved_piece,side,LIST) -> int:
    promo_list = (b.WQ,b.WR,b.WN,b.WB) if moved_piece == b.WP else (b.BQ,b.BR,b.BN,b.BB)
    for promotion in promo_list:
        b.PROMOTION_PIECE = promotion
        Board.Move_attacker(from_sq, to_sq)
        legal_check = Board.Check_state(side)
        if not legal_check:
            LIST.append((from_sq, to_sq, moved_piece,promotion,))
        Board.Undo_move()

def All_legal_move(side):
    LEGAL_MOVES = []
    for from_sq, from_mask in mog.MOVES_DICT.items():
        m = from_mask
        while m:
            lsb = m & -m
            to_sq = lsb.bit_length() - 1
            m ^= lsb

            moved_piece = b.SQUARE_MAP[from_sq]

            if (moved_piece == b.WP and to_sq > 55 and side == 0) or \
               (moved_piece == b.BP and to_sq < 8 and side == 1):
                promotion_append(from_sq,to_sq,moved_piece,side,LEGAL_MOVES)
                continue  

            Board.Move_attacker(from_sq, to_sq)
            if not Board.Check_state(side):
                LEGAL_MOVES.append((from_sq, to_sq, moved_piece))
            Board.Undo_move()

    return LEGAL_MOVES