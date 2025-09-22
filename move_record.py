import bitboard as b

# === explanation for move_record.py ===
# This module defines classes to record chess moves and evaluations.
# The MoveRecord class captures details of each move, including the starting and ending squares,
# the piece moved, any captured piece, special move flags (like castling or promotion), and the en passant square.

# The EvalRecord class stores the evaluation scores for both white and black players at a given point in the game.
# These records are essential for implementing features like undoing moves and maintaining game state.
# The module is designed to work with a chess engine that uses bitboards for efficient board representation and move generation.


#==========================================Move Record Class=================================================
class MoveRecord:
    NONE_FLAG = 0
    EN_PASSANT_FLAG = 1
    CASTLE_FLAG = 2
    PROMOTION_FLAG = 3
    
    def __init__(self, from_sq, to_sq, moved_piece, captured_piece, en_sq,promotion_piece,flags=0,castling_rights=None):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.moved_piece = moved_piece
        self.captured_piece = captured_piece
        self.flags = flags
        self.en_sq = en_sq
        self.promotion_piece = promotion_piece
        self.castling_rights = castling_rights

#==========================================Evaluation Record Class=================================================
class EvalRecord:
    def __init__(self,white_score,black_score):
        self.white_score = white_score
        self.black_score = black_score


