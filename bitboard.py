
BIT_BOARD = [None,None,None,None] 
#Start occupancy squars
BIT_BOARD[0] =0xff00              #WHITE_PAWN
BIT_BOARD[1] =0xff000000000000    #BLACK_PAWN
BIT_BOARD[2] =0xff                #WHITE_FIRST_ROW
BIT_BOARD[3] =0xff00000000000000  #BLACK_FIRST_ROW

pieces = ["P", "N", "B", "R", "Q", "K","p", "n", "b", "r", "q", "k"]
#Piece that hold all pieces squares


EMPTY, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK = range(13)
PIECE_BITBOARDS = [0] * 13

PIECE_DICT = {piece: 0 for piece in pieces}
PIECES_TURN = []
#Row pieces for occupancy squars
WHITE_ROW1_PIECES = ["R","N","B","Q","K","B","N","R"]
BLACK_ROW1_PIECES = ["r","n","b","q","k","b","n","r"]

#Occupancy squars divide for color
WHITE_OCCUPANCY = 0
BLACK_OCCUPANCY = 0
ALL_OCCUPANCY = 0

CASTLING_WHITE_KING = 0x60
CASTLING_WHITE_QUEEN = 0xe
CASTLING_BLACK_KING = 0x6000000000000000
CASTLING_BLACK_QUEEN = 0xe00000000000000

LIGHT_SQUARE = 0x55aa55aa55aa55aa
DARK_SQUARE = 0xaa55aa55aa55aa55


SQUARE_MAP = [
    "R","N","B","Q","K","B","N","R",
    "P","P","P","P","P","P","P","P",
    ".",".",".",".",".",".",".",".",
    ".",".",".",".",".",".",".",".",
    ".",".",".",".",".",".",".",".",
    ".",".",".",".",".",".",".",".",
    "p","p","p","p","p","p","p","p",
    "r","n","b","q","k","b","n","r",
]
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

        
