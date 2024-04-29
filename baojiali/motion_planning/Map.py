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
import enum
NodeType = enum.Enum('NodeType', ('C', 'P', 'E','N'))

class Node:
    def __init__(self,x,y,type=NodeType.N):
        self.x=x
        self.y=y
        self.type=type

class Edge:
    def __init__(self,node0:Node,node1:Node,weight):
        self.node0=node0
        self.node1=node1
        self.weight=weight

class NodeMap:
    def __init__(self):
        self.nodes=set()
        self.edges=set()
    
    def add_node(self,node:Node):
        self.nodes.add(node)
        
    def add_edge(self,edge:Edge):
        self.edges.add(edge)
        if edge.node0 not in self.nodes:
            self.nodes.add(edge.node0)
        if edge.node1 not in self.nodes:
            self.nodes.add(edge.node1)
        
def draw_NodeMap(nodeMap:NodeMap):
    for edge in nodeMap.edges:
        pass
    pass

def main():
    edges=[]
    edge0=Edge(node0=Node(x=100,y=100,type=NodeType.P),node1=Node(x=200,y=200,type=NodeType.P),weight=200)
    nodeMap=NodeMap()
    nodeMap.add_edge(edge0)
    draw_NodeMap(nodeMap)
    

if __name__ == '__main__':
    main()
        