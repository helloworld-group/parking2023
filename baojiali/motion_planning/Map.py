import matplotlib.pyplot as plt
import numpy as np
class GridMap:
    def __init__(self,width,height) -> None:
        self.width=width
        self.height=height
        self.grid=[[0]*self.width for _ in range(self.height)]

    def print(self):
        for row in self.grid:
            print(row)

    def neighbors(self,row,col):
        result=[]
        dirs=[[-1,0],[1,0],[0,-1],[0,1]]
        for dir in dirs:
            next_row=row+dir[0]
            next_col=col+dir[1]
            if next_row <0 or next_row>=self.height:
                continue
            if next_col <0 or next_col>=self.width:
                continue
            if self.grid[next_row][next_col]==1:
                continue
            result.append([next_row,next_col])
        return result

    def plot(self):
        plt.imshow(self.grid)
        plt.show()
    
    def add_obstacle(self,row,col,width,height):
        """_summary_

        Args:
            row (int): _description_
            col (int): _description_
            width (int): _description_
            height (int): _description_
        """
        if row<0 or row>=len(self.grid):
            return
        if col<0 or col>=len(self.grid[0]):
            return
        for i in range(row,row+height):
            for j in range(col,col+width):
                self.grid[i][j]=1