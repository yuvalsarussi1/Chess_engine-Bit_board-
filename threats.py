import bitboard as b
import moves as mo
class Threats:

    THREAT_MAP_WHITE = 0
    THREAT_MAP_BLACK = 0

    @staticmethod
    def white_squares() -> list[int]:
        squares_white = []
        bits = b.WHITE_OCCUPANCY
        while bits:
            lsb = bits & -bits
            sq = (lsb.bit_length() - 1)
            squares_white.append(sq)
            bits &= bits - 1
        return squares_white

    @staticmethod
    def black_squares() -> list[int]:
        squares_black = []
        bits = b.BLACK_OCCUPANCY
        while bits:
            lsb = bits & -bits
            sq = (lsb.bit_length() - 1)
            squares_black.append(sq)
            bits &= bits - 1
        return squares_black

    @classmethod
    def get_threat_map_white(cls):
        import moves as mo
        cls.THREAT_MAP_WHITE = 0
        for square in cls.white_squares():
            attacks = mo.Piece_attack(square)
            cls.THREAT_MAP_WHITE |= attacks
        return cls.THREAT_MAP_WHITE

    @classmethod
    def get_threat_map_black(cls):
        import moves as mo
        cls.THREAT_MAP_BLACK = 0
        for square in cls.black_squares():
            attacks = mo.Piece_attack(square)
            cls.THREAT_MAP_BLACK |= attacks
        return cls.THREAT_MAP_BLACK


    @classmethod
    def threat_map_update(cls):
        cls.get_threat_map_white()
        cls.get_threat_map_black()
        return cls.THREAT_MAP_WHITE,cls.THREAT_MAP_BLACK


    def square_attacked_by_black(sq: int) -> bool:
        if mo.Pawn_attacks_eat_black(sq)    & b.PIECE_DICT[b.BP]: return True
        if mo.Knight_attacks(sq)            & b.PIECE_DICT[b.BN]: return True
        if mo.Bishop_attack(sq)             & (b.PIECE_DICT[b.BB] | b.PIECE_DICT[b.BQ]): return True
        if mo.Rook_attack(sq)               & (b.PIECE_DICT[b.BR] | b.PIECE_DICT[b.BQ]): return True
        if mo.King_attack_black(sq)         & b.PIECE_DICT[b.BK]: return True
        return False

    def square_attacked_by_white(sq: int) -> bool:
        if mo.Pawn_attacks_eat_white(sq)    & b.PIECE_DICT[b.WP]: return True
        if mo.Knight_attacks(sq)            & b.PIECE_DICT[b.WN]: return True
        if mo.Bishop_attack(sq)             & (b.PIECE_DICT[b.WB] | b.PIECE_DICT[b.WQ]): return True
        if mo.Rook_attack(sq)               & (b.PIECE_DICT[b.WR] | b.PIECE_DICT[b.WQ]): return True
        if mo.King_attack_white(sq)               & b.PIECE_DICT[b.WK]: return True
        return False
