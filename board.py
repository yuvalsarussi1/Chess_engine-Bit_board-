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
    
    def Move_attacker(square_num: int,target: int,attack_name: str):
        square_index = (1 << square_num)
        target_index = (1 << target)
        
        PIECE_DICT[attack_name] &= ~square_index
        PIECE_DICT[attack_name] |=target_index
    def Remove_target(target: int,target_name: str):
        target_index = (1 << target)
        PIECE_DICT[target_name] &= ~ target_index
        

        



    def print_board():
        pass



# Board.Fresh_reset()
# Board.Update_occupancy()

# print(hex(WHITE_OCCUPANCY))

     








# Board.Fresh_reset()
# Board.Update_occupancy()
# check = Board.Piece_existence_check(1<<57,WHITE_OCCUPANCY)
# print(check)







