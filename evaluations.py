import bitboard as b
import evaluation_tables as ev
import move_record as mr

# === explanation for evaluations.py ===
# This module handles the evaluation of the chess board state for both players.
# It maintains evaluation scores for white and black, updates these scores based on piece movements and captures,
# and provides functions to undo evaluations when moves are reverted.

# Piece values for evaluation
PIECE_SCORES = {
    b.WP: 100, b.WN: 320, b.WB: 330, b.WR: 500, b.WQ: 900, b.WK: 0,
    b.BP: 100, b.BN: 320, b.BB: 330, b.BR: 500, b.BQ: 900, b.BK: 0
}

# Global evaluation scores
TOTAL_EVAL = 0
BLACK_EVAL = 0
WHITE_EVAL = 0
CURRENT_EVAL = 0



# evaluation maps for positional scoring
evaluation_maps = [ev.PAWN_SCORE_TABLE,ev.KNIGHT_SCORE_TABLE,ev.BISHOP_SCORE_TABLE,
                   ev.ROOK_SCORE_TABLE,ev.QUEEN_SCORE_TABLE,ev.KING_SCORE_TABLE
                   ]

# update evaluation based on piece capture
def capture_evaluation(to_sq, captured_piece) -> None:
    global WHITE_EVAL, BLACK_EVAL
    if captured_piece == b.E:
        return
    if captured_piece <= b.WK:  # White piece captured
        WHITE_EVAL -= PIECE_SCORES[captured_piece] + evaluation_maps[captured_piece - 1][63 - to_sq]
    else:  # Black piece captured
        BLACK_EVAL -= PIECE_SCORES[captured_piece] + evaluation_maps[captured_piece - 7][to_sq]


# update evaluation based on piece movement
def position_evaluation_map(from_sq, to_sq, moved_piece) -> None:
    global WHITE_EVAL, BLACK_EVAL

    
    eval_record = mr.EvalRecord(WHITE_EVAL,BLACK_EVAL)
    b.EVAL_HISTORY.append(eval_record)

    if moved_piece == b.E:
        return
    if moved_piece == b.WK or moved_piece == b.BK:
        return  

    
    if moved_piece <= b.WK:  
        score_table = evaluation_maps[moved_piece - 1]
        current_score = score_table[63 - from_sq]
        new_score     = score_table[63 - to_sq]
        WHITE_EVAL += (new_score - current_score)
    else:  
        score_table = evaluation_maps[moved_piece - 7]
        current_score = score_table[63 - to_sq]
        new_score     = score_table[63 - from_sq]
        BLACK_EVAL += (new_score - current_score)

# undo the last evaluation update
def engine_eval_undo() -> None:
    global WHITE_EVAL, BLACK_EVAL
    eval = b.EVAL_HISTORY.pop()
    white_eval, black_eval = eval.white_score, eval.black_score
    WHITE_EVAL = white_eval
    BLACK_EVAL = black_eval

# check if the engine is in a favorable position
def engine_eval_condition(ENGINE_SIDE) -> bool:
    if ENGINE_SIDE == 0:
        if WHITE_EVAL > BLACK_EVAL:return True
        else: return False
    




    