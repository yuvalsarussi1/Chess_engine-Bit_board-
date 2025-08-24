def Coord_converter(square : str) -> int: #Take coord (a2) turn into Bit index
        if len(square) == 2:
            file = ord(square[0].lower()) - ord("a")
            if (0 <= file <= 7) and (square[1].isdigit()):   
                rank = int(square[1]) - 1                  
                if (0 <= rank <= 7):
                    index = rank * 8 + file                    
                    return 1 << index
                return 0       
            return 0 
        return False      