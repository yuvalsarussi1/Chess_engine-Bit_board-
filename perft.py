import board as bo
import fen as fe
import move_generate as mog
import legal_moves as ch

def perft(depth, side):
    if depth == 0:
        return 1

    nodes = 0
    mog.All_Move_generate()
    legal_moves = ch.All_legal_move(side)
    for move in legal_moves:
        from_sq, to_sq, moved_piece, *rest = move
        bo.Board.Move_attacker(from_sq, to_sq)
        if not bo.Board.Check_state(side):
            nodes += perft(depth - 1, 1 - side)
        bo.Board.Undo_move()

    return nodes


def perft_test(fen_code="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", max_depth=3):
    side = fe.Fen.FEN_Option(fen_code)
    for d in range(1, max_depth + 1):
        nodes = perft(d, side)
        print(f"perft({d}) = {nodes}")


