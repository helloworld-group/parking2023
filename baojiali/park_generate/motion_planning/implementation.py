# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

from __future__ import annotations
# some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
import math
T = TypeVar('T')

# Location = TypeVar('Location')

# class Location():
#     def __init__(self,x:float,y:float,id:int=-1) -> None:
#         self.x = x
#         self.y = y
#         self.id=id
        
        
class Node():
    counter = 0
    def __init__(self,x,y,id=None) -> None:
        if id:
            self.id=id
        else:
            self.id=Node.counter
            Node.counter+=1
        self.x=x
        self.y=y
        

                
class Graph():
    def __init__(self):
        self.edges: dict[int, list[int]] = {}
        self.nodes:dict[int,Node]={}
        
    def add_edge(self, u: int, v: int):
        """在两个已有的节点之间添加一条边"""
        if u in self.nodes and v in self.nodes:
            if u not in self.edges:
                self.edges[u] = []
            self.edges[u].append(v)
    # def add_edge(self, id1: int, id2: int):
    #     # self.nodes.setdefault
    #     self.edges.setdefault(id1, []).append(id2)
    #     # self.edges.setdefault(id2, []).append(id1)
    
    def add_node(self,node:Node):
        """将一个节点添加到图中"""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.edges[node.id] = []
        # self.nodes[id]=node
        
    def neighbors(self, location: Node) -> list[Node]: 
        neighbord=[]
        for neighbor_id in self.edges[location.id]:
            neighbord.append(self.nodes[neighbor_id])

        return neighbord
    
    def get_limit(self)-> tuple[int,int,int,int]:
        x=list()
        y=list()
        for node_id,location in self.nodes.items():
            x.append(location.x)
            y.append(location.y)
        xmin=min(x)
        xmax=max(x)
        ymin=min(y)
        ymax=max(y)
        return xmin,ymin,xmax,ymax
    
    def get_location(self,id:int)->Node:
        if id in self.nodes.keys():
            return self.nodes[id]
        
    def insert_node_in_edge(self, u: int, v: int, new_node: Node):
        """在边 (u, v) 中插入新节点 new_node"""
        if u in self.edges and v in self.edges[u]:
            self.add_node(new_node)       # 添加新节点 new_node
            self.edges[u].remove(v)       # 移除原来的边 (u, v)
            self.add_edge(u, new_node.id) # 添加新的边 (u, new_node)
            self.add_edge(new_node.id, v) # 添加新的边 (new_node, v)
        

class SimpleGraph:
    def __init__(self):
        self.edges: dict[Node, list[Node]] = {}
    
    def neighbors(self, id: Node) -> list[Node]:
        return self.edges[id]

import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self) -> T:
        return self.elements.popleft()

# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

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

# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in [21,22,51,52,81,82,93,94,111,112,123,124,133,134,141,142,153,154,163,164,171,172,173,174,175,183,184,193,194,201,202,203,204,205,213,214,223,224,243,244,253,254,273,274,283,284,303,304,313,314,333,334,343,344,373,374,403,404,433,434]]

GridLocation = Tuple[int, int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class WeightedGraph(Graph):
    # def cost(self, from_id: int, to_id: int) -> float:
    #     if to_id in self.edges[from_id]:
    #         location_from=self.nodes[from_id]
    #         location_to=self.nodes[to_id]
            
    #         return math.sqrt(location_from.x-location_to.x)**2+(location_from.y-location_to.y)**2
    #     else:
    #         return None
    def cost(self, from_location: Node, to_location: Node) -> float:
        if to_location.id in self.edges[from_location.id]:
            
            return math.sqrt((from_location.x-to_location.x)**2+(from_location.y-to_location.y)**2)
        else:
            return None

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
        self.seen_priorities=set()
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        if priority not in self.seen_priorities:
            heapq.heappush(self.elements, (priority, item))
            self.seen_priorities.add(priority)
    
    def get(self) -> T:
        priority,item=heapq.heappop(self.elements)
        self.seen_priorities.remove(priority)
        return item
def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from: dict[Location, Location],
                     start: Location, goal: Location) -> list[Location]:

    current: Location = goal
    path: list[Location] = []
    if goal not in came_from: # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

diagram_nopath = GridWithWeights(10, 10)
diagram_nopath.walls = [(5, row) for row in range(10)]


def heuristic(a: Node, b: Node) -> float:
    (x1, y1) = a.x,a.y
    (x2, y2) = b.x,b.y
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: WeightedGraph, start: Node, goal: Node):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Node, Optional[Node]] = {}
    cost_so_far: dict[Node, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Node = frontier.get()
        
        if current == goal:
            return came_from, cost_so_far
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return (None,None)

def breadth_first_search(graph: Graph, start: Location, goal: Location)->dict[Location, Optional[Location]] :
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    return came_from

class SquareGridNeighborOrder(SquareGrid):
    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x + dx, y + dy) for (dx, dy) in self.NEIGHBOR_ORDER]
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)

def test_with_custom_order(neighbor_order):
    if neighbor_order:
        g = SquareGridNeighborOrder(30, 15)
        g.NEIGHBOR_ORDER = neighbor_order
    else:
        g = SquareGrid(30, 15)
    g.walls = DIAGRAM1_WALLS
    start, goal = (8, 7), (27, 2)
    came_from = breadth_first_search(g, start, goal)
    draw_grid(g, path=reconstruct_path(came_from, start=start, goal=goal),
              point_to=came_from, start=start, goal=goal)

class GridWithAdjustedWeights(GridWithWeights):
    def cost(self, from_node, to_node):
        prev_cost = super().cost(from_node, to_node)
        nudge = 0
        (x1, y1) = from_node
        (x2, y2) = to_node
        if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        return prev_cost + 0.001 * nudge