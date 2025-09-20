import board as bo
import fen as fe
import move_generate as mog
import legal_moves as ch
from utils import *
from castling import ca
import move_record as mr
piece_counters = {
    b.WP: 0, b.WN: 0, b.WB: 0, b.WR: 0, b.WQ: 0, b.WK: 0,
    b.BP: 0, b.BN: 0, b.BB: 0, b.BR: 0, b.BQ: 0, b.BK: 0,
}



def print_piece_counts(counters):
    piece_names = {
        b.WP: "WP",   b.WN: "WN", b.WB: "WB",
        b.WR: "WR",   b.WQ: "WQ",  b.WK: "WK",
        b.BP: "BP",   b.BN: "BN", b.BB: "BB",
        b.BR: "BR",   b.BQ: "BQ",  b.BK: "BK",
    }

    for piece, name in piece_names.items():
        print(f"{name}: {counters[piece]}")


def count_piece_move(moved_piece, counters):
    if moved_piece in counters:
        counters[moved_piece] += 1


def perft(depth, side):
    if depth == 0:
        return 1
    nodes = 0

    Update_PIECES_TURN(side)
    mog.All_Move_generate()
    legal_moves = ch.All_legal_move(side)

    for move in legal_moves:
        from_sq, to_sq, moved_piece, *rest = move
        captured_piece = 0
        w,captured_piece,flags = bo.Board.Move_attacker(from_sq, to_sq)
        if not bo.Board.Check_state(side):
            if depth == 1:
                nodes += 1
                # track check stats
                if bo.Board.Check_state(1 - side):
                    b.CHECKS += 1
                # Track captures
                if captured_piece != 0 or flags == mr.MoveRecord.EN_PASSANT_FLAG:
                    b.CAPTURES += 1
                if flags == mr.MoveRecord.CASTLE_FLAG:
                    b.CASTLING += 1
            else:   
                nodes += perft(depth - 1, 1 - side)

        bo.Board.Undo_move()
    
    return nodes


def perft_test(fen_code="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", max_depth=3):
    side = fe.Fen.FEN_Option(fen_code)
    for d in range(1, max_depth + 1):
        
        b.CHECKS = 0
        b.CAPTURES = 0
        b.CHECKMATES = 0
        b.CASTLING = 0
        nodes = perft(d, side)
        print(f"perft({d}) = {nodes}")
        print(f"  checks: {b.CHECKS}")
        print(f"  captures: {b.CAPTURES}")
        print(f"  checkmates: {b.CHECKMATES}")
        print(f"  castling: {b.CASTLING}")

