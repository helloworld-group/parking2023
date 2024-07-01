# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

from __future__ import annotations
# some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
import math
from math_tool import distance2segment

T = TypeVar('T')
class Node():
    counter = 0
    def __init__(self,x,y,id=None) -> None:
        if not id is None:
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
        else:
            if u not in self.edges:
                self.edges[u] = []
            self.edges[u].append(v)
            
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
        
        if v in self.edges and u in self.edges[v]:
            self.add_node(new_node)       # 添加新节点 new_node
            self.edges[v].remove(u)       # 移除原来的边 (v, u)
            self.add_edge(v, new_node.id) # 添加新的边 (v, new_node)
            self.add_edge(new_node.id, u) # 添加新的边 (new_node, u)
  
        
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


class WeightedGraph(Graph):
    def cost(self, from_location: Node, to_location: Node) -> float:
        if to_location.id in self.edges[from_location.id]:
            
            return math.sqrt((from_location.x-to_location.x)**2+(from_location.y-to_location.y)**2)
        else:
            return None
        
        
    def get_closest_edge(self,x:float,y:float)-> Tuple[float,Tuple[np.array],float]:
        min_distance=float('inf')
        min_edge_start=None
        min_edge_end=None
        min_proj_point=None
        
        for edge_start,edge_ends in self.edges.items():
            for edge_end in edge_ends:
                P=(x,y)
                edge_start_node=self.nodes[edge_start]
                edge_end_node=self.nodes[edge_end]
                A=(edge_start_node.x,edge_start_node.y)
                B=(edge_end_node.x,edge_end_node.y)
                distance,proj_point=distance2segment(P,A,B)
                
                if distance<min_distance:
                    min_distance=distance
                    min_edge_start_node=edge_start
                    min_edge_end_node=edge_end
                    min_proj_point=proj_point

        return min_edge_start_node,min_edge_end_node,min_distance,min_proj_point




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




def heuristic(a: Node, b: Node) -> float:
    (x1, y1) = a.x,a.y
    (x2, y2) = b.x,b.y
    return math.sqrt(abs(x1 - x2) + abs(y1 - y2))


def a_star_search(graph: WeightedGraph, start: Node, goal: Node):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Node, Optional[Node]] = {}
    cost_so_far: dict[Node, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Node = frontier.get()
        # print(current.id)
        if current == goal:
            return came_from, cost_so_far
        
        for next in graph.neighbors(current):
            if next.id==86:
                aaaa=1
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                heuristic_value=heuristic(next, goal)
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return (None,None)

