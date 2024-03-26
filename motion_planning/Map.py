import matplotlib.pyplot as plt
import numpy as np


def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)


class GridMap:
    def __init__(self,width,height) -> None:
        self.width=width
        self.height=height
        self.grid=[[0]*self.width for _ in range(self.height)]

    def print(self):
        for row in self.grid:
            print(row)

    def neighbors(self,node):
        result=[]
        dirs=[[-1,0],[1,0],[0,-1],[0,1]]
        for dir in dirs:
            next_row,next_col=node[0]+dir[0],node[1]+dir[1]
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
    
    def add_obstacles(self,obstacles):
        """_summary_

        Args:
            obstacles (_type_): _description_
        """
        for obstacle in obstacles:
            row,col=obstacle
            if row<0 or row>=len(self.grid):
                return
            if col<0 or col>=len(self.grid[0]):
                return
            self.grid[row][col]=1

class WeightedGraph:
    pass