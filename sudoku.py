class InputError(Exception):
    pass

class Game(object):
    def __init__(self, positions):
        self.initial_cells = set()
        self.__create_board(positions)
        
    def __create_board(self, positions):
        self.initial_board = { (i,j):None for i in range(9) for j in range(9) }
        for p in positions:
            if len(p) != 3:
                raise InputError(str(p) + " is not length 3")
            self.initial_board[(p[0],p[1])] = p[2]
            self.initial_cells.add( (p[0],p[1]))
        self.board = self.initial_board.copy()
        
    def reset_board(self):
        self.board = self.initial_board.copy()
            
    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return (False, "Row {} is not good".format(row+1))
        for column in range(9):
            if not self.__check_column(column):
                return (False, "Column {} is not good".format(column+1))
        for x in range(3):
            for y in range(3):
                if not self.__check_block(x,y):
                    return (False, "Block ({},{}) is not good".format(x+1,y+1))
        return (True,"It looks good")
      
    def __check_zone(self,numbers):
        return set(numbers) == set(range(1,10))
        
    def __check_row(self,r):
        return self.__check_zone([self.board[(r,j)] for j in range(9)])
    
    def __check_column(self,c):
        return self.__check_zone([self.board[(i,c)] for i in range(9)])
    
    def __check_block(self,x,y):
        return self.__check_zone([self.board[(3*x+i,3*y+j) ] for i in range(3) for j in range(3)])
    