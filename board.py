import bitboard as b


class Board:
    def __init__(self):
        self.reset()

    @staticmethod
    def Fresh_reset():
        # Assign individual pieces to main dict PIECE_DICT
        for square_1 in range(8):
            #PIECE_DICT --> (P:1 << 8)
            b.PIECE_DICT["P"] |= (1 << (8 + square_1))
            b.PIECE_DICT["p"] |= (1 << (48 + square_1))
            b.PIECE_DICT[b.WHITE_ROW1_PIECES[square_1]] |= (1 << square_1) 
            b.PIECE_DICT[b.BLACK_ROW1_PIECES[square_1]] |= (1 << (56 + square_1)) 

    @staticmethod
    def Update_occupancy():
        #Creat the occupancy or update it
        global WHITE_OCCUPANCY,BLACK_OCCUPANCY,ALL_OCCUPANCY,PIECE_DICT

        b.WHITE_OCCUPANCY =  (b.PIECE_DICT["P"] | b.PIECE_DICT["N"] | b.PIECE_DICT["B"]|
                            b.PIECE_DICT["R"] | b.PIECE_DICT["Q"] | b.PIECE_DICT["K"])
        b.BLACK_OCCUPANCY =  (b.PIECE_DICT["p"] | b.PIECE_DICT["n"] | b.PIECE_DICT["b"]|
                            b.PIECE_DICT["r"] | b.PIECE_DICT["q"] | b.PIECE_DICT["k"])
        b.ALL_OCCUPANCY   = b.BLACK_OCCUPANCY | b.WHITE_OCCUPANCY
        
    
    def piece_exists(bit_index: int, occupancy: int) -> bool:
        """Check if a piece exists at the given bit index in the occupancy bitboard."""
        return (occupancy & (1 << bit_index)) != 0
    
    def Move_attacker(from_sq: int,to_sq: int):
        
        from_sq_index = (1 << from_sq)
        to_sq_index = (1 << to_sq)
        
        Attacker_sq = b.SQUARE_MAP[from_sq]
        Enemy_sq = b.SQUARE_MAP[to_sq]

        b.PIECE_DICT[Attacker_sq] &= ~from_sq_index
        b.PIECE_DICT[Attacker_sq] |=to_sq_index
        if Enemy_sq != ".":
            b.PIECE_DICT[Enemy_sq] &= ~to_sq_index
        
        b.SQUARE_MAP[from_sq] = "."
        b.SQUARE_MAP[to_sq] = Attacker_sq

    def print_board_list(lst, top_down=True):
        rows = [lst[i:i+8] for i in range(0, len(lst), 8)]
        if top_down:
            rows = rows[::-1]   # flip order for rank 8 at top
        for row in rows:
            print(" ".join(row))

        



     











