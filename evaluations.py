import bitboard as b
import evaluation_tables as ev
import move_record as mr

PIECE_SCORES = {
    b.WP: 100, b.WN: 320, b.WB: 330, b.WR: 500, b.WQ: 900, b.WK: 0,
    b.BP: 100, b.BN: 320, b.BB: 330, b.BR: 500, b.BQ: 900, b.BK: 0
}

TOTAL_EVAL = 0
BLACK_EVAL = 0
WHITE_EVAL = 0
CURRENT_EVAL = 0




evaluation_maps = [ev.PAWN_SCORE_TABLE,ev.KNIGHT_SCORE_TABLE,ev.BISHOP_SCORE_TABLE,
                   ev.ROOK_SCORE_TABLE,ev.QUEEN_SCORE_TABLE,ev.KING_SCORE_TABLE
                   ]




def capture_evaluation(to_sq, captured_piece):
    global WHITE_EVAL, BLACK_EVAL
    if captured_piece == b.E:
        return
    if captured_piece <= b.WK:  # White piece captured
        WHITE_EVAL -= PIECE_SCORES[captured_piece] + evaluation_maps[captured_piece - 1][63 - to_sq]
    else:  # Black piece captured
        BLACK_EVAL -= PIECE_SCORES[captured_piece] + evaluation_maps[captured_piece - 7][to_sq]


# side_score()
# print("Initial White Eval:", WHITE_EVAL)
# print("Initial Black Eval:", TOTAL_EVAL)
# print("Initial Total Eval (White - Black):", WHITE_EVAL - TOTAL_EVAL)



def position_evaluation_map(from_sq, to_sq, moved_piece):
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
        current_score = score_table[to_sq]
        new_score     = score_table[from_sq]
        BLACK_EVAL += (new_score - current_score)

    






def engine_eval_undo():
    global WHITE_EVAL, BLACK_EVAL
    eval = b.EVAL_HISTORY.pop()
    white_eval, black_eval = eval.white_score, eval.black_score
    WHITE_EVAL = white_eval
    BLACK_EVAL = black_eval

    
def engine_eval_condition(ENGINE_SIDE):
    if ENGINE_SIDE == 0:
        if WHITE_EVAL > BLACK_EVAL:return True
        else: return False
    




    