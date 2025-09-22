import bitboard as b

# === explanation for fen.py ===
# This module handles the Forsyth-Edwards Notation (FEN) for representing chess positions.
# It includes a Fen class that can parse a FEN string to extract the board layout,
# side to move, castling rights, en passant target square, and move counters.
# The module provides methods to convert the FEN representation into internal data structures,
# such as piece dictionaries and square maps, which are used by the chess engine.
# It also includes several example FEN strings for common chess positions.

# === Example FEN strings ===
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"          # STARTING BOARD
"rnb1kbnr/pppp1ppp/8/4p3/6Pq/8/PPPPP2P/RNBQKBNR w KQkq - 0 3"       # FOOL'S MATE CHECKMATE IN 2
"rnbqkbnr/pp1ppppp/8/2p5/4PP2/8/PPPP2PP/RNBQKBNR b KQkq f3 0 2"     # EN PASSANT SETUP
"r3k2r/pppqppbp/2np1np1/8/2BPP3/2N2N2/PPP2PPP/R1BQ1RK1 w k - 4 8"   # CASTLING TEST
"4k3/5P2/8/8/8/8/8/4K3 w - - 0 1"                                   # PROMOTION




class Fen:
    # Constants for pieces
    E, P, N, B, R, Q, K, p, n, b, r, q, k = range(13)

    # Mapping from FEN characters to piece constants
    fen_map = {
    "P": P, "N": N, "B": B, "R": R, "Q": Q, "K": K,
    "p": p, "n": n, "b": b, "r": r, "q": q, "k": k,
    }
    
    # Attributes for FEN components
    def __init__(self,mask,turn,castling_rights,ep_target_sq,half_move,full_move):
        self.mask = mask
        self.turn = turn
        self.castling_rights = castling_rights
        self.en_target_sq = ep_target_sq
        self.half_move = half_move
        self.full_move = full_move

    # Static method to split a FEN string into its components
    def split_fen(fen_string) -> 'Fen':
        #take a fen string and return a Fen object with attributes
        fen = fen_string
        fen_split = fen.split(" ")
        fen_obj = Fen(fen_split[0],fen_split[1],fen_split[2],fen_split[3],fen_split[4],fen_split[5])
        return fen_obj
    
    # Convert the board part of the FEN into a list of piece constants
    def board_mask(fen_obj) -> list:
        ranks = fen_obj.mask.split("/")   # don’t reverse
        board = []
        for rank in reversed(ranks):      # go from rank 8 → rank 1
            for char in rank:
                if char.isdigit():
                    board.extend([Fen.E] * int(char))
                else:
                    board.append(Fen.fen_map[char])
        return board

    # Update the piece list based on the FEN board
    def Piece_list_fen(board) -> None:
        for piece in range(len(b.PIECE_DICT)):
            b.PIECE_DICT[piece] = 0

        b.WHITE_OCCUPANCY = 0
        b.BLACK_OCCUPANCY = 0
        b.ALL_OCCUPANCY = 0

        for sq, val in enumerate(board):
            if val != 0:
                b.PIECE_DICT[val] |= 1 << sq
                b.ALL_OCCUPANCY |= 1 << sq
                if val <= b.WK:   # white pieces
                    b.WHITE_OCCUPANCY |= 1 << sq
                    if val == b.WK:
                        b.WHITE_KING_SQ = sq
                else:             # black pieces
                    b.BLACK_OCCUPANCY |= 1 << sq
                    if val == b.BK:
                        b.BLACK_KING_SQ = sq

    # Update the square map based on the FEN board
    def Square_map_fen(board) -> None:
        for i in range(64):
            b.SQUARE_MAP[i] = board[i]

    # Determine which side is to move based on the FEN
    def side_to_move(fen_obj) -> int:
        side = fen_obj.turn
        if side == "b":
            return 1
        else:
            return 0
        
    # Update castling rights based on the FEN
    def castling_fen(fen_obj) -> None:
        rights = fen_obj.castling_rights
        print("DEBUG: FEN rights =", rights)
        b.CASTLING_WK = "K" in rights
        b.CASTLING_WQ = "Q" in rights
        b.CASTLING_BK = "k" in rights
        b.CASTLING_BQ = "q" in rights
        print("DEBUG: WK,WQ,BK,BQ =", b.CASTLING_WK, b.CASTLING_WQ, b.CASTLING_BK, b.CASTLING_BQ)

    # Update the en passant square based on the FEN
    def en_passant_fen(fen_obj) -> None:
        ep_str = fen_obj.en_target_sq
        if ep_str == "-":
            return -1  # or None
        file = ord(ep_str[0]) - ord('a')
        rank = int(ep_str[1]) - 1
        b.EN_PASSANT_SQ = rank * 8 + file
          
    # Update move counters based on the FEN
    def Moves(fen_obj) -> None:
        b.HALF_MOVE = int(fen_obj.half_move)
        b.FULL_MOVE = int(fen_obj.full_move)

    # Main method to process a FEN string and update the board state
    @staticmethod
    def FEN_Option(fen_code)-> int:
        fen_obj = Fen.split_fen(fen_code)
        board = Fen.board_mask(fen_obj)
        side = Fen.side_to_move(fen_obj)
        
        Fen.castling_fen(fen_obj)
        Fen.en_passant_fen(fen_obj)
        Fen.Moves(fen_obj)
        Fen.Piece_list_fen(board)
        Fen.Square_map_fen(board)
        
        return side







