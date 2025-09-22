import board as bo
import fen as fe
import move_generate as mog
import legal_moves as ch
from utils import *
from castling import ca
import move_record as mr


"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # starting position

"r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1" # castling

"4k3/5P2/8/8/8/8/8/4K3 w - - 0 1" # promotion
















def perft(depth, side):
    if depth == 0:
        return 1
    nodes = 0

    Update_PIECES_TURN(side)
    mog.All_Move_generate()
    legal_moves = ch.All_legal_move(side)



    for move in legal_moves:
        from_sq, to_sq, moved_piece, *rest = move
        Promotion = rest[0] if rest else None
        b.PROMOTION_PIECE = Promotion if Promotion else 0 
        captured_piece = 0
        w,captured_piece,flags = bo.Board.Move_attacker(from_sq, to_sq)
        if not bo.Board.Check_state(side):
            if depth == 1:
                nodes += 1
                
                
                if bo.Board.Check_state(1 - side):
                    b.CHECKS += 1                        
                if captured_piece != 0:
                    b.CAPTURES += 1
                if flags == mr.MoveRecord.CASTLE_FLAG:
                    b.CASTLING += 1
                if flags == mr.MoveRecord.EN_PASSANT_FLAG:
                    b.EN_PASSANT_CAPTURE += 1
                if flags == mr.MoveRecord.PROMOTION_FLAG:
                    b.PROMOTIONS += 1
                # print(nodes,b.ALL_OCCUPANCY)

            else:   
                nodes += perft(depth - 1, 1 - side)
                

        bo.Board.Undo_move()
    
    return nodes


def perft_test(fen_code="r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", max_depth=3):
    side = fe.Fen.FEN_Option(fen_code)
    print("Beforemove",b.ALL_OCCUPANCY)
    for d in range(1, max_depth + 1):
        
        b.CHECKS = 0
        b.CAPTURES = 0
        b.CHECKMATES = 0
        b.CASTLING = 0
        b.EN_PASSANT_CAPTURE = 0
        b.PROMOTIONS = 0

        nodes = perft(d, side)
        print(f"perft({d}) = {nodes}")
        print(f"  checks: {b.CHECKS}")
        print(f"  captures: {b.CAPTURES + b.EN_PASSANT_CAPTURE}")
        print(f"  checkmates: {b.CHECKMATES}")
        print(f"  castling: {b.CASTLING}")
        print(f"  en_passant: {b.EN_PASSANT_CAPTURE}")
        print(f"  promotions: {b.PROMOTIONS}")



