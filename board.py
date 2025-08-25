from bitboard import *


class Board:
    def __init__(self):
        self.reset()


    def Fresh_reset():
        # Assign individual pieces to main dict PIECE_DICT
        for square_1 in range(8):
            #PIECE_DICT --> (P:1 << 8)
            PIECE_DICT["P"] |= (1 << (8 + square_1))
            PIECE_DICT["p"] |= (1 << (48 + square_1))
            PIECE_DICT[WHITE_ROW1_PIECES[square_1]] |= (1 << square_1) 
            PIECE_DICT[BLACK_ROW1_PIECES[square_1]] |= (1 << (56 + square_1)) 


    def Update_occupancy():
        #Creat the occupancy or update it
        global WHITE_OCCUPANCY,BLACK_OCCUPANCY,ALL_OCCUPANCY

        WHITE_OCCUPANCY =  (PIECE_DICT["P"] | PIECE_DICT["N"] | PIECE_DICT["B"]|
                            PIECE_DICT["R"] | PIECE_DICT["Q"] | PIECE_DICT["K"])
        BLACK_OCCUPANCY =  (PIECE_DICT["p"] | PIECE_DICT["n"] | PIECE_DICT["b"]|
                            PIECE_DICT["r"] | PIECE_DICT["q"] | PIECE_DICT["k"])
        ALL_OCCUPANCY = BLACK_OCCUPANCY | WHITE_OCCUPANCY


    def piece_exists(bit_index: int, occupancy: int) -> bool:
        """Check if a piece exists at the given bit index in the occupancy bitboard."""
        return (occupancy & (1 << bit_index)) != 0
    
    def Move_execute():
        pass

    def print_board():
        pass


     








Board.Fresh_reset()
Board.Update_occupancy()
check = Board.Piece_existence_check(1<<57,WHITE_OCCUPANCY)
print(check)







