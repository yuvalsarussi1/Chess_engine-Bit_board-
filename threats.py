import bitboard as b

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
    def get_threat_map(cls):
        cls.get_threat_map_white()
        cls.get_threat_map_black()
        return cls.THREAT_MAP_WHITE,cls.THREAT_MAP_BLACK

