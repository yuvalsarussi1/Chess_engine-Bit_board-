

import bitboard as b
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

        
    def __repr__(self):
        return (f"MoveRecord(from_sq={self.from_sq}, to_sq={self.to_sq}, moved_piece={self.moved_piece}, "
                f"captured_piece={self.captured_piece}, promotion_piece={self.promotion_piece}, "
                f"is_castling={self.is_castling}, en_passant_square={self.en_passant_square})")

    
class En_passant:
    def __init__(self,R_cell,L_cell,condition):
        self.R_cell = R_cell
        self.L_cell = L_cell
        self.codition = False

class EvalRecord:
    def __init__(self,white_score,black_score):
        self.white_score = white_score
        self.black_score = black_score


