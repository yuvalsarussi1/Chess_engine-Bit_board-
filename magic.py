# import _init_
import bitboard as b
# import random (for fidding magic numbers)

# ==== explanation of magic bitboards ====
# A magic bitboard is a way to efficiently calculate the attack patterns of sliding pieces
# (rooks and bishops) in chess. The idea is to use a "magic" number to transform the
# occupancy of the board into an index that can be used to look up the attack pattern
# in a precomputed table. This allows for very fast move generation, as it reduces
# the need for complex calculations during gameplay.

#the magic numbers are calculated using a brute-force method to find numbers that produce
#unique indices for all possible blocker configurations for each square on the board.
# These numbers are then used in conjunction with bitwise operations to quickly
# determine the attack patterns of rooks and bishops.


#========================================Creat magic numbers===========================================
MAGIC_NUMBER_ROOK_LIST = [
    36029349996072992,        9259423098992599040,   756622329720602752,
    1224984115168739336,      720578140611616772,    432363405522239748,
    10988802882270142720,     2341871944762134656,   9224216601371623680,
    4689936478589960704,      1689125317115920,      2882444705165475968,
    2360167752733819268,     1153203015119012096,   4756082698693378816,
    2331316576210411648,     8647193859584950344,   422763294826496,
    378867517946757185,       144397762701557794,    1154188691892241408,
    396458056096941056,       9732877063655522,      4614010386281398401,
    4611723953726046209,      1171261916908224768,   14510616695382475842,
    9262215729670275090,      4612064256870056320,   562958544929808,
    288318354262353417,       1153202983878543746,   9331459664874832068,
    9011872321773696,         4512412902367232,      146411037090914560,
    140771856499712,          180425494548712448,    218426953353433089,
    31526850987557444,        70405797281793,        72655797103902720,
    144172639739576352,       144362578460606476,    2252351784124424,
    45038195364102272,        10088152844361531426,  2458967097355665409,
    35734157262976,           2343068094351544704,   4785143860445440,
    1766000402902286464,      10522801301199519872,  1261570864559688192,
    16285412146047683584,     286427078459904,       106652904718401,
    1409712419537937,         105553267331265,       2306124639347146761,
    18577503352293386,        9570269740468226,      11529295379950993924,
    144396688831029825
]

MAGIC_NUMBER_BISHOP_LIST = [
    18089270560441088,        1152297585477632,         9225632634011385936,
    598709851390088,          1131811124543624,         9296855835181384192,
    288521266034526336,       216194781071279104,       226358797554222404,
    74921569157376,           8935161486293926408,      216491683469592576,
    4755859550413260800,      144724321881948160,       9223601028440535040,
    10135307076899328,        1126039627630592,         941463565825507584,
    1011058185066268688,      142008899682304,          307377823585140992,
    10273871144093804,        4648739533234176,         9241632729207408648,
    47323050252839424,        4621258918042272768,      578715919505703170,
    294994573842317344,       180426559686983697,       4504149400134784,
    5836955663053882369,      1302925918077600,         155550212084990528,
    324910092645303822,       14988159884633047298,     6918657128752742529,
    9224533129723781248,      38280876005560320,        326590142386028816,
    7066748157819896836,      55740859735344400,        288520722450550800,
    1153486679386898688,      9512446975660787712,      36037799539900674,
    577041441014956544,       146375942963462464,       2319354435970531458,
    2306168473515721360,      1689547927224832,         436920099543734273,
    1189937664175251458,      2485995859221815809,      36600659165970496,
    9946217442382514432,      4638708767251398784,      108231543822222080,
    36029900834997248,        72110382412222464,        72621093764241409,
    20301417860432384,        69269457600,              5119397039970368,
    153158132279820416
]

def bit_count(bb: int) -> int:
    return bin(bb).count("1")
#========================================Creat relevent bit===========================================
#Relevant bits are all the possible blocker pieces for each square
def init_rook_relevant_bits():
    
    global ROOK_RELEVANT_BITS
    ROOK_RELEVANT_BITS = [bit_count(b.ROOK_EXCLUDE_EDGES[sq]) for sq in range(64)]

def init_bishop_relevant_bits():
    global BISHOP_RELEVANT_BITS
    BISHOP_RELEVANT_BITS = [bit_count(b.BISHOP_EXCLUDE_EDGES[sq]) for sq in range(64)]

#========================================check the magic number for generate===========================================
#after finding a magic number we need to check if its valid
# MAGIC_ATTACKS_ROOK = [[] for i in range(64)]
def Check_valid_magic_number_rook(magic_num: int,square: int):
    temp_list = {}
    bits = ROOK_RELEVANT_BITS[square]
    size = 1 << bits
    for subset_sq, attack_sq in zip(b.ROOK_BLOCKER_SUBSET[square], b.ROOK_ATTACKS_NO_MAGIC[square]):
        index = ((subset_sq * magic_num) & ((1 << 64) - 1)) >> (64 - bits)        # print(b.ROOK_BLOCKER_SUBSET[0][1], "blocker subset")
        if index >= size:         
            # print("bad magic size")
            return False
        
        if index in temp_list and temp_list[index] != attack_sq:
            # print("bad magic dupe")
            return False
        temp_list[index] = attack_sq
    # print("good magic")
    
    return magic_num
# MAGIC_ATTACKS_BISHOP = [[] for i in range(64)]
def Check_valid_magic_number_bishop(magic_num: int,square: int):
    temp_list = {}
    bits = BISHOP_RELEVANT_BITS[square]
    size = 1 << bits
    for subset_sq, attack_sq in zip(b.BISHOP_BLOCKER_SUBSET[square], b.BISHOP_ATTACKS_NO_MAGIC[square]):
        index = ((subset_sq * magic_num) & ((1 << 64) - 1)) >> (64 - bits)        # print(b.ROOK_BLOCKER_SUBSET[0][1], "blocker subset")
        if index >= size:         
            # print("bad magic size")
            return False
        
        if index in temp_list and temp_list[index] != attack_sq:
            # print("bad magic dupe")
            return False
        temp_list[index] = attack_sq
    # print("good magic")
    
    return magic_num



#========================================Creat magic attacks===========================================
#create the magic attacks for each square and store them in a list
MAGIC_ATTACKS_ROOK = [[] for i in range(64)]
def Creat_magic_attacks_rook(magic_num: int,square: int):
    bits = ROOK_RELEVANT_BITS[square]
    list_size = 1 << bits
    MAGIC_ATTACKS_ROOK[square] = [0] * list_size
    for subset_sq, attack_sq in zip(b.ROOK_BLOCKER_SUBSET[square], b.ROOK_ATTACKS_NO_MAGIC[square]):
        index = ((subset_sq * magic_num) & ((1 << 64) - 1)) >> (64 - bits)
        if index >= list_size:
            print("error")
            return False
        MAGIC_ATTACKS_ROOK[square][index] = attack_sq
    # print("good")
    return True

def Creat_rook_attacks_all_squares():
    for square in range(64):
        magic_num = MAGIC_NUMBER_ROOK_LIST[square]
        if magic_num == 0:
            print("no magic number")
            return False
        check = Creat_magic_attacks_rook(magic_num,square)
        if check is False:
            print("error creating magic attacks")
            return False
    return True


MAGIC_ATTACKS_BISHOP = [[] for i in range(64)]
def Creat_magic_attacks_bishop(magic_num: int,square: int):
    bits = BISHOP_RELEVANT_BITS[square]
    list_size = 1 << bits
    MAGIC_ATTACKS_BISHOP[square] = [0] * list_size
    
    
    for subset_sq, attack_sq in zip(b.BISHOP_BLOCKER_SUBSET[square], b.BISHOP_ATTACKS_NO_MAGIC[square]):
        index = ((subset_sq * magic_num) & ((1 << 64) - 1)) >> (64 - bits)
        if index >= list_size:
            print("error")
            return False
        MAGIC_ATTACKS_BISHOP[square][index] = attack_sq
    # print("good")
    return True

def Creat_bishop_attacks_all_squares():
    for square in range(64):
        magic_num = MAGIC_NUMBER_BISHOP_LIST[square]
        if magic_num == 0:
            print("no magic number")
            return False
        check = Creat_magic_attacks_bishop(magic_num,square)
        if check is False:
            print("error creating magic attacks")
            return False
    return True




#========================================INIT ALL THE THINGS===========================================

#this function is for fidding magic numbers

# MAGIC_NUMBER_BISHOP_LIST = [0]*64
# for square in range(64):
#     for i in range(1_000_000):
#         magic_number = (random.getrandbits(64) & random.getrandbits(64) & random.getrandbits(64))
#         magic_num = m.Check_valid_magic_number_bishop(magic_number,square)
#         if magic_num != False:
#             print(magic_num)
#             check = m.Creat_magic_attacks_bishop(magic_num,square)
#             if check is True:
#                 print(f"square {square}: found magic {hex(magic_number)}")
#                 MAGIC_NUMBER_BISHOP_LIST[square] = magic_num
#                 break
#             else:
#                 print("error creating magic attacks")
# print(MAGIC_NUMBER_BISHOP_LIST)















