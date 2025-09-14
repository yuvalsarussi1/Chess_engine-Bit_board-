import bitboard as b






# --- FENS ---
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"          # STARTING BOARD
"rnb1kbnr/pppp1ppp/8/4p3/6Pq/8/PPPPP2P/RNBQKBNR w KQkq - 0 3"       # FOOL'S MATE CHECKMATE IN 2
"rnbqkbnr/pp1ppppp/8/2p5/4PP2/8/PPPP2PP/RNBQKBNR b KQkq f3 0 2"     # EN PASSANT SETUP
"r3k2r/pppqppbp/2np1np1/8/2BPP3/2N2N2/PPP2PPP/R1BQ1RK1 w k - 4 8"   # CASTLING TEST
"4k3/5P2/8/8/8/8/8/4K3 w - - 0 1"                                   # PROMOTION




class Fen:
    
    E, P, N, B, R, Q, K, p, n, b, r, q, k = range(13)

    fen_map = {
    "P": P, "N": N, "B": B, "R": R, "Q": Q, "K": K,
    "p": p, "n": n, "b": b, "r": r, "q": q, "k": k,
    }

    def __init__(self,mask,turn,castling_rights,ep_target_sq,half_move,full_move):
        self.mask = mask
        self.turn = turn
        self.castling_rights = castling_rights
        self.en_target_sq = ep_target_sq
        self.half_move = half_move
        self.full_move = full_move


    def split_fen(fen_string):
        fen = fen_string
        fen_split = fen.split(" ")
        fen_obj = Fen(fen_split[0],fen_split[1],fen_split[2],fen_split[3],fen_split[4],fen_split[5])
        return fen_obj
    

    def board_mask(fen_obj):
        ranks = fen_obj.mask.split("/")
        ranks = list(reversed(ranks))
        board = []
        for rank in ranks:
            for char in rank:
                if char.isdigit():
                    board.extend([Fen.E] * int(char))  # empty squares
                else:
                    board.append(Fen.fen_map[char])               # piece
        return board
    
    def Piece_dict_fen(board):
        for piece in range(len(b.PIECE_DICT)):
            b.PIECE_DICT[piece] = 0
        
        
        for sq, val in enumerate(board):
            if val != 0:
                b.PIECE_DICT[val] |= 1 << sq
            
    def Square_map_fen(board):
        b.SQUARE_MAP = board

    def side_to_move(fen_obj):
        side = fen_obj.turn
        if side == "b":
            return 1
        else:
            return 0
        
    
    def castling_fen(fen_obj): # need optimaize wite bool conditions
        rights = fen_obj.castling_rights
        b.CASTLING_WK = "K" in rights
        b.CASTLING_WQ = "Q" in rights
        b.CASTLING_BK = "k" in rights
        b.CASTLING_BQ = "q" in rights
        
        if rights != "-":
            for char in rights:
                if char == "K":
                    b.CASTLING_WK = True
                if char == "Q":
                    b.CASTLING_WQ = True
                if char == "k":
                    b.CASTLING_BK = True
                if char == "q":
                    b.CASTLING_BQ = True


    def en_passant_fen(fen_obj):
        ep_str = fen_obj.en_target_sq
        if ep_str == "-":
            return -1  # or None
        file = ord(ep_str[0]) - ord('a')
        rank = int(ep_str[1]) - 1
        return rank * 8 + file
        
    def Moves(fen_obj):
        b.HALF_MOVE = int(fen_obj.half_move)
        b.FULL_MOVE = int(fen_obj.full_move)


    @staticmethod
    def FEN_Option(fen_code):
        fen_obj = Fen.split_fen(fen_code)
        board = Fen.board_mask(fen_obj)
        side = Fen.side_to_move(fen_obj)
        
        Fen.castling_fen(fen_obj)
        Fen.en_passant_fen(fen_obj)
        Fen.Moves(fen_obj)
        Fen.Piece_dict_fen(board)
        Fen.Square_map_fen(board)
        
        return side







