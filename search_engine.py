import board as bo
import move_generate as mog
import legal_moves as ch
from utils import *
import evaluations as ev

#=== explanation for search_engine.py ===

# This module implements a search engine for a chess game using the minimax algorithm with alpha-beta pruning.
# The Search_engine function recursively explores possible moves to a specified depth, evaluating the board state
# at each leaf node. It aims to find the best move for the engine's side by maximizing its score while minimizing
# the opponent's score. The Search_engine_eval function iteratively deepens the search, providing the best move found at each depth level.

# example of search tree:
#=====================================================================
#                 White to move (MAX)                   depth == 3 
#                /          |          \
#           Move A        Move B          Move C        depth == 2 
#          /    \         /    \         /     \        
#         A1    A2       B1    B2       C1     C2       depth == 1
#        / \    / \     / \    / \     / \    /  \
#       5   7  3   2   8   6  4   9   1   0  7    2     depth == 0 
#=====================================================================



# The engine uses evaluation functions from the evaluations module to assess board states
def Search_engine(depth: int, side: int, ENGINE_SIDE: int,alpha=-999999, beta=999999) -> tuple[int, tuple]:
    if depth == 0:
        return ev.WHITE_EVAL - ev.BLACK_EVAL, None

    Update_PIECES_TURN(side)
    mog.All_Move_generate()
    legal_moves = ch.All_legal_move(side)


    if not legal_moves:
        if bo.Board.Check_state(side):
            # Mate found
            mate_score = (100000 - (depth)) if side != ENGINE_SIDE else -(100000 - depth)
            return mate_score, None
        else:
            return 0, None



    if side == 0:  # White = maximize
        best_score = -999999
    else:          # Black = minimize
        best_score = 999999
    best_move = None




    for move in legal_moves:
        from_sq, to_sq, moved_piece, *rest = move
        b.PROMOTION_PIECE = rest[0] if rest else None

        m, captured_piece, flags = bo.Board.Move_attacker(from_sq, to_sq)
        ev.position_evaluation_map(from_sq, to_sq, moved_piece)
        ev.capture_evaluation(to_sq, captured_piece)
        score, _ = Search_engine(depth - 1, 1 - side, ENGINE_SIDE, alpha, beta)

        ev.engine_eval_undo()
        bo.Board.Undo_move()

        
        if side == 0:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:  # prune
                break
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:  # prune
                break

    return best_score, best_move

# execute the best move found by the search engine
def Search_engine_eval(depth,side):
    b.ENGINE_SIDE = side
    best_move = None
    best_score = 0

    for branch in range(1,depth + 1):
        score,move = Search_engine(branch,side,b.ENGINE_SIDE)
        if move:
            best_move = move
            best_score = score
        print(f"Depth {branch}: score {score}, best move {move}")
    if best_move:
        bo.Board.Move_attacker(best_move[0],best_move[1])
    
    return best_score, best_move



