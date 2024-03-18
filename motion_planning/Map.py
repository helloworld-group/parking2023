import matplotlib as plt
class GridMap:
    def __init__(self,width,height) -> None:
        self.width=width
        self.height=height
        self.grid=[[0]*self.width for _ in range(self.height)]

    def print(self):
        for row in self.grid:
            print(row)
    def plot(self):

        pass
    
    def add_obstacle(self,row,col,width,height):
        """_summary_

        Args:
            row (_type_): _description_
            col (_type_): _description_
            width (_type_): _description_
            height (_type_): _description_
        """
        if row<0 or row>=len(self.grid):
            return
        if col<0 or col>=len(self.grid[0]):
            return
        for i in range(row,row+height):
            for j in range(col,col+width):
                self.grid[i][j]=1