
BIT_BOARD = [None,None,None,None] 
#Start occupancy squars
BIT_BOARD[0] =0xff00              #WHITE_PAWN
BIT_BOARD[1] =0xff000000000000    #BLACK_PAWN
BIT_BOARD[2] =0xff                #WHITE_FIRST_ROW
BIT_BOARD[3] =0xff00000000000000  #BLACK_FIRST_ROW

pieces = ["P", "N", "B", "R", "Q", "K","p", "n", "b", "r", "q", "k"]
#Piece that hold all pieces squares


E = 2
E, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK = range(13)
PIECE_BITBOARDS = [0] * 13


MOVE_HISTORY = []


PIECE_DICT = [0]*13
PIECES_TURN = []
#Row pieces for occupancy squars
WHITE_ROW1_PIECES = [WR,WN,WB,WQ,WK,WB,WN,WR]
BLACK_ROW1_PIECES = [BR,BN,BB,BQ,BK,BB,BN,BR]

#Occupancy squars divide for color
WHITE_OCCUPANCY = 0
BLACK_OCCUPANCY = 0
ALL_OCCUPANCY = 0

CASTLING_WHITE_KING_SIDE = 0x60
CASTLING_WHITE_QUEEN_SIDE = 0xe
CASTLING_BLACK_KING_SIDE = 0x6000000000000000
CASTLING_BLACK_QUEEN_SIDE = 0xe00000000000000

WHITE_KING_MOVE = 0
BLACK_KING_MOVE = 0
WHITE_RR_MOVE = 0
WHITE_LR_MOVE = 0
BLACK_RR_MOVE = 0
BLACK_LR_MOVE = 0

# White castling empty squares
WHITE_KINGSIDE_EMPTY   = (1 << 5) | (1 << 6)           
WHITE_QUEENSIDE_EMPTY  = (1 << 1) | (1 << 2) | (1 << 3) 

# Black castling empty squares
BLACK_KINGSIDE_EMPTY   = (1 << 61) | (1 << 62)          
BLACK_QUEENSIDE_EMPTY  = (1 << 57) | (1 << 58) | (1 << 59) 







LIGHT_SQUARE = 0x55aa55aa55aa55aa
DARK_SQUARE = 0xaa55aa55aa55aa55

SQUARE_MAP = [
    WR, WN, WB, WQ, WK, WB, WN, WR,   # 0–7   White back rank
    WP, WP, WP, WP, WP, WP, WP, WP,   # 8–15  White pawns
    E, E, E, E, E, E, E, E,   # 16–23
    E, E, E, E, E, E, E, E,   # 24–31
    E, E, E, E, E, E, E, E,   # 32–39
    E, E, E, E, E, E, E, E,   # 40–47
    BP, BP, BP, BP, BP, BP, BP, BP,   # 48–55 Black pawns
    BR, BN, BB, BQ, BK, BB, BN, BR    # 56–63 Black back rank
]

PIECE_TO_CHAR = {
    E: ".",
    WP: "P", WN: "N", WB: "B", WR: "R", WQ: "Q", WK: "K",
    BP: "p", BN: "n", BB: "b", BR: "r", BQ: "q", BK: "k"
}

WHITE_KING_SQ = 4
BLACK_KING_SQ = 60


WHITE_SCORE = 0
BLACK_SCORE = 0

PIECE_SCORES = {
    "P": 1,   
    "N": 3,   
    "B": 3,   
    "R": 5,   
    "Q": 9,   
    "K": 0,   

    "p": 1,   
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0
}




#==========================================General Pieces Mask=================================================

"""Creating all the walkable squares from each square for every piece """

KNIGHT_MASK = [0]*64
def init_Knight_mask():
    #all possible knight moves
    jumps = [(2,1),(2,-1),(1,2),(1,-2),(-2,-1),(-2,1),(-1,-2),(-1,2)]
    #Create the mask
    for num in range(64):
        x = num % 8
        y = num // 8
        for dx,dy in jumps:
            if (0 <= dx + x < 8) and (0 <= dy + y < 8):
                KNIGHT_MASK[num] |= (1 << (dy + y)*8 + (dx + x))


KING_SIDE_CASTLING_MASK_WHITE = 0x40
QUEEN_SIDE_CASTLING_MASK_WHITE = 0x4

KING_SIDE_CASTLING_MASK_BLACK = 0x4000000000000000
QUEEN_SIDE_CASTLING_MASK_BLACK = 0x400000000000000
KING_MASK = [0]*64
def init_King_mask():
    #all possible king moves
    jumps = [(1,0),(1,-1),(1,1),(0,1),(0,-1),(-1,0),(-1,1),(-1,-1)]
    #Create the mask
    for num in range(64):
        x = num % 8
        y = num // 8
        for dx,dy in jumps:
            if (0 <= dx + x < 8) and (0 <= dy + y < 8):
                KING_MASK[num] |= (1 << (dy + y)*8 + (dx + x))

    




PAWN_MASK_WALK_WHITE = [0]*64
PAWN_MASK_EAT_WHITE  = [0]*64
PAWN_MASK_ENPASSANT_WHITE = [0]*64
PAWN_MASK_DOUBLE_WHITE = [0]*64

PAWN_MASK_WALK_BLACK = [0]*64
PAWN_MASK_EAT_BLACK  = [0]*64
PAWN_MASK_ENPASSANT_BLACK = [0]*64
PAWN_MASK_DOUBLE_BLACK = [0]*64
def init_Pawn_mask():
    for num in range(64):
        x = num % 8
        y = num // 8
        if y < 7:
            PAWN_MASK_WALK_WHITE[num] |= (1 << ((y+1)*8 + x))
            if y == 1:
                PAWN_MASK_ENPASSANT_WHITE[num] |= (1 << ((y+2)*8 + x))
                PAWN_MASK_DOUBLE_WHITE[num] |= (1 << ((y+2)*8 + x))
            if x > 0:
                PAWN_MASK_EAT_WHITE[num] |= (1 << ((y+1)*8 + (x-1)))
            if x < 7:
                PAWN_MASK_EAT_WHITE[num] |= (1 << ((y+1)*8 + (x+1)))
            
        
        if y > 0:
            PAWN_MASK_WALK_BLACK[num] |= (1 << ((y-1)*8 + x))
            if y == 6:
                PAWN_MASK_ENPASSANT_BLACK[num] |= (1 << ((y-2)*8 + x))
                PAWN_MASK_DOUBLE_BLACK[num] |= (1 << ((y-2)*8 + x))
            if x > 0:
                PAWN_MASK_EAT_BLACK[num] |= (1 << ((y-1)*8 + (x-1)))
            if x < 7:
                PAWN_MASK_EAT_BLACK[num] |= (1 << ((y-1)*8 + (x+1)))
        
ROOK_MASK = [0]*64
def init_Rook_mask():
    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    #Create the mask
    for i in range(64):
        x = i % 8
        y = i // 8
        for dx,dy in directions:
            cx = dx + x
            cy = dy + y
            while ((0 <= cx < 8) and (0 <= cy < 8)):
                ROOK_MASK[i] |= 1 << (cx + cy*8)
                cx += dx
                cy += dy
    

BISHOP_MASK = [0]*64
def init_Bishop_mask():
    #all possible bishop ray moves
    directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
    #Create the mask
    for i in range(64):
        x = i % 8
        y = i //8
        for dx,dy in directions:
            cx = dx + x
            cy = dy + y
            while ((0 <= cx < 8) and (0 <= cy < 8)):
                BISHOP_MASK[i] |= 1 << (cx + cy*8)
                cx += dx
                cy += dy

QUEEN_MASK = [0]*64
def init_Queen_mask():
    directions = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]

    for i in range(64):
        x = i % 8
        y = i //8
        for dx,dy in directions:
            cx = dx + x
            cy = dy + y
            while ((0 <= cx < 8) and (0 <= cy < 8)):
                QUEEN_MASK[i] |= 1 << (cx + cy*8)
                cx += dx
                cy += dy


#===========================================================================================

#==========================================Exclude Edges Pieces Mask=================================================

"""Same as piece mask but without the edges"""

ROOK_EXCLUDE_EDGES = [0]*64
def init_Rook_exclude_edges():
    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    #Creat the mask
    for i in range(64):
        x = i % 8
        y = i // 8
        mask = 0
        for dx,dy in directions:
            cx = x + dx
            cy = y + dy
            while ((0 <= cx < 8) and (0 <= cy < 8)):
                cx += dx
                cy += dy
            mask |= 1 << ((cx-dx) + ((cy-dy)*8))
        ROOK_EXCLUDE_EDGES[i] = ROOK_MASK[i] & ~mask
    


BISHOP_EXCLUDE_EDGES = [0]*64
def init_Bishop_exclude_edges():
    directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
    #Creat the mask
    for i in range(64):
        x = i % 8
        y = i // 8
        mask = 0
        for dx,dy in directions:
            cx = x + dx
            cy = y + dy
            while ((0 <= cx < 8) and (0 <= cy < 8)):
                cx += dx
                cy += dy
            mask |= 1 << ((cx-dx) + ((cy-dy)*8))
        BISHOP_EXCLUDE_EDGES[i] = BISHOP_MASK[i] & ~mask

QUEEN_EXCLUDE_EDGES = [0]*64
def init_Queen_exclude_edges():
    for i in range(64):
        QUEEN_EXCLUDE_EDGES[i] = ROOK_EXCLUDE_EDGES[i] | BISHOP_EXCLUDE_EDGES[i]


#===========================================================================================

#==========================================blocker subsets=================================================

"""Creating all the possible subset from each square for sliding pieces"""

ROOK_BLOCKER_SUBSET = [[] for i in range(64)]
def init_Rook_blocker_subset_build():
    for i in range(64):
        mask = ROOK_EXCLUDE_EDGES[i]
        subset = 0
        while True:
            ROOK_BLOCKER_SUBSET[i].append(subset)
            subset = (subset - mask) & mask
            if subset == 0:
                break

BISHOP_BLOCKER_SUBSET = [[] for i in range(64)]
def init_Bishop_blocker_subset_build():
    for i in range(64):
        mask = BISHOP_EXCLUDE_EDGES[i]
        subset = 0
        while True:
            BISHOP_BLOCKER_SUBSET[i].append(subset)
            subset = (subset - mask) & mask
            if subset == 0:
                break
            

""" QUEEN --> Will combine both Bishop and Rook subset"""
""" Making Queen subset will make millions of subset  """


#===========================================================================================

ROOK_ATTACKS_NO_MAGIC = [[] for i in range(64)]
def init_Rook_attack_no_magic():
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for square in range(64):
        ROOK_ATTACKS_NO_MAGIC[square] = []
        x = square % 8
        y = square // 8
        for blocker_subset in ROOK_BLOCKER_SUBSET[square]:
            mask = 0
            for dx, dy in directions:
                cx, cy = x + dx, y + dy
                while 0 <= cx < 8 and 0 <= cy < 8:
                    sq = cx + cy*8        # <- explicit square index
                    mask |= (1 << sq)
                    if blocker_subset & (1 << sq):
                        break             # stop immediately at first blocker
                    cx += dx
                    cy += dy
            ROOK_ATTACKS_NO_MAGIC[square].append(mask)

BISHOP_ATTACKS_NO_MAGIC = [[] for i in range(64)]
def init_Bishop_attack_no_magic():
    directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
    for square in range(64):
        x = square % 8
        y = square // 8
        for blocker_subset in BISHOP_BLOCKER_SUBSET[square]:
            mask = 0
            for dx,dy in directions:
                cx = x + dx
                cy = y + dy
                while ((0 <= cx < 8) and (0 <= cy < 8)):
                    mask |= (1 << (cx + cy*8))
                    if blocker_subset & (1 << (cx + (cy*8))):
                        break
                    cx += dx
                    cy += dy
            BISHOP_ATTACKS_NO_MAGIC[square].append(mask)

        
