BIT_BOARD = [None,None,None,None] 
#Start occupancy squars
BIT_BOARD[0] =0xff00              #WHITE_PAWN
BIT_BOARD[1] =0xff000000000000    #BLACK_PAWN
BIT_BOARD[2] =0xff                #WHITE_FIRST_ROW
BIT_BOARD[3] =0xff00000000000000  #BLACK_FIRST_ROW

pieces = ["P", "N", "B", "R", "Q", "K","p", "n", "b", "r", "q", "k"]
#Piece that hold all pieces squares
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

PAWN_MASK_WALK = [0]*64
PAWN_MASK_EAT = [0]*64
PAWN_MASK_ENPASSANT = [0]*64
def init_Pawn_mask():
    jumps_walk = (0,1)
    jump_eat = [(1,1),(-1,1)]
    jump_enpassant = (0,2)
    for num in range(64):
        x = num % 8
        y = num // 8
        ax,ay = jumps_walk
        if (0 <= ax + x < 8) and (0 <= ay + y < 8):
            PAWN_MASK_WALK[num] |= (1 << (ay + y)*8 + (ax + x))
        bx,by = jump_enpassant
        if (0 <= bx + x < 8) and (0 <= by + y < 8):
            PAWN_MASK_ENPASSANT[num] |= (1 << (by + y)*8 + (bx + x))
        for cx,cy in jump_eat:
            if (0 <= cx + x < 8) and (0 <= cy + y < 8):
                PAWN_MASK_EAT[num] |= (1 << (cy + y)*8 + (cx + x))
        
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
        subset = ROOK_EXCLUDE_EDGES[i]
        while True:
            ROOK_BLOCKER_SUBSET[i].append(subset) 
            if subset == 0:
                break
            subset = (subset - 1) & ROOK_EXCLUDE_EDGES[i]

BISHOP_BLOCKER_SUBSET = [[] for i in range(64)]
def init_Bishop_blocker_subset_build():
    for i in range(64):
        subset = BISHOP_EXCLUDE_EDGES[i]
        while True:
            BISHOP_BLOCKER_SUBSET[i].append(subset) 
            if subset == 0:
                break
            subset = (subset - 1) & BISHOP_EXCLUDE_EDGES[i]

""" QUEEN --> Will combine both Bishop and Rook subset"""
""" Making Queen subset will make millions of subset  """


#===========================================================================================

#==========================================Generate attack=================================================
"""Creating all the possible attack bitboard from each square for sliding pieces based on blocker subset"""

ROOK_ATTACKS = [[] for i in range(64)]
def Rook_attack():
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for square in range(64):
        attack_subset = ROOK_BLOCKER_SUBSET[square]
        for blocker_subset in attack_subset:
            x = square % 8
            y = square // 8
            mask = 0
            for dx,dy in directions:
                cx = x + dx
                cy = y + dy
                while ((0 <= cx < 8) and (0 <= cy < 8)):
                    mask |= (1 << (cx + cy*8))
                    if (blocker_subset & (1 << (cx + (cy*8)))): 
                        break
                    cx += dx
                    cy += dy
            ROOK_ATTACKS[square].append(mask)    
    
BISHOP_ATTACKS = [[] for i in range(64)]
def Bishop_attack():
    directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
    for square in range(64):
        attack_subset = BISHOP_BLOCKER_SUBSET[square]
        for blocker_subset in attack_subset:
            x = square % 8
            y = square // 8
            mask = 0
            for dx,dy in directions:
                cx = x + dx
                cy = y + dy
                while ((0 <= cx < 8) and (0 <= cy < 8)):
                    mask |= (1 << (cx + cy*8))
                    if (blocker_subset & (1 << (cx + (cy*8)))): 
                        break
                    cx += dx
                    cy += dy
            BISHOP_ATTACKS[square].append(mask)

""" QUEEN --> Will combine both Bishop and Rook attacks"""
""" Making Queen subset will make millions of attacks  """
    


        

