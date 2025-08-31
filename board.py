import bitboard as b
import threats as th
import utils as u
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
        
    
    def piece_exists(square_num: int, occupancy: int) -> bool:
        """Check if a piece exists at the given bit index in the occupancy bitboard."""
        return (occupancy & (1 << square_num)) != 0
    
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




        # # --- Incremental occupancy updates ---
        # b.ALL_OCCUPANCY ^= from_sq_index
        # b.ALL_OCCUPANCY |= to_sq_index

        # if Attacker_sq.isupper():  # white move
        #     b.WHITE_OCCUPANCY ^= from_sq_index
        #     b.WHITE_OCCUPANCY |= to_sq_index
        # else:                      # black move
        #     b.BLACK_OCCUPANCY ^= from_sq_index
        #     b.BLACK_OCCUPANCY |= to_sq_index

        # if Enemy_sq != ".":  # captured piece clears occupancy
        #     if Enemy_sq.isupper():
        #         b.WHITE_OCCUPANCY ^= to_sq_index
        #     else:
        #         b.BLACK_OCCUPANCY ^= to_sq_index


    # def Update_oc(from_sq: int,to_sq: int):

    #     from_sq_index = (1 << from_sq)
    #     to_sq_index = (1 << to_sq)
        
    #     Attacker_sq = b.SQUARE_MAP[from_sq]
    #     Enemy_sq = b.SQUARE_MAP[to_sq]


    #     # --- Incremental occupancy updates ---
    #     b.ALL_OCCUPANCY ^= from_sq_index
    #     b.ALL_OCCUPANCY |= to_sq_index

    #     if Attacker_sq.isupper():  # white move
    #         b.WHITE_OCCUPANCY ^= from_sq_index
    #         b.WHITE_OCCUPANCY |= to_sq_index
    #     else:                      # black move
    #         b.BLACK_OCCUPANCY ^= from_sq_index
    #         b.BLACK_OCCUPANCY |= to_sq_index

    #     if Enemy_sq != ".":  # captured piece clears occupancy
    #         if Enemy_sq.isupper():
    #             b.WHITE_OCCUPANCY ^= to_sq_index
    #         else:
    #             b.BLACK_OCCUPANCY ^= to_sq_index





    def print_board_list(lst, top_down=True):
        rows = [lst[i:i+8] for i in range(0, len(lst), 8)]
        if top_down:
            rows = rows[::-1]   # flip order for rank 8 at top
        for row in rows:
            print(" ".join(row))

    

    def Check_state(side) -> bool:
        if side == "w" and (th.Threats.THREAT_MAP_BLACK & b.PIECE_DICT["K"]):
            return True
        if side == "b" and (th.Threats.THREAT_MAP_WHITE & b.PIECE_DICT["k"]):
            return True
        return False


    def Undo_move(from_sq: int,to_sq: int,moved_piece: str,captured_piece: str):
        
        from_sq_index = (1 << from_sq)
        to_sq_index = (1 << to_sq)

        Attacker_sq = b.SQUARE_MAP[from_sq]
        Enemy_sq = b.SQUARE_MAP[to_sq]
       
        #Reset moved piece to previos state
        b.PIECE_DICT[moved_piece] &= ~to_sq_index
        b.PIECE_DICT[moved_piece] |=from_sq_index
        
        #Reset captured piece to previos state
        if captured_piece != ".":
            b.PIECE_DICT[captured_piece] |= to_sq_index
        b.SQUARE_MAP[to_sq] = captured_piece
        b.SQUARE_MAP[from_sq] = moved_piece

        #Reset occupancy to previos state
        Board.Update_occupancy()
        


        #Reset occupancy to previos state
        th.Threats.threat_map_update()

        #Reset turn to previos state
        # flip_side = u.Side_change(side)
        # print(flip_side,"Turn")
        











