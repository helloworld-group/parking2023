import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List,Dict,Tuple,Optional
from datetime import datetime
from motion_planning.graph import WeightedGraph,Node
from math_tool import distance2segment
# from park_analysis.park_utils import

class ParkingSlot():
    def __init__(self,id:int,x: float,y:float):
        self.id=id
        self.x=x
        self.y=y
        
class Light():
    def __init__(self,id:int,x:float,y:float):
        self.id=id
        self.x=x
        self.y=y
        self.lighting_periods=[]
    
    def is_activated_by_path_section(self,node_0:Node,node_1:Node,threshold=4.2)->bool:
        P=(self.x,self.y)
        A=(node_0.x,node_0.y)
        B=(node_1.x,node_1.y)
        distance,proj_point=distance2segment(P,A,B)
        # print(distance)
        if distance<threshold:
            return True
        return False

    def is_activated_by_node(self,node:Node,threshold=3)->bool:
        distance=math.sqrt((self.x-node.x)**2+(self.y-node.y)**2)
        # print(distance)
        if distance<threshold:
            return True
        return False
    
    def add_period(self,start_time:datetime,end_time:datetime):
        self.lighting_periods.append([start_time,end_time])
        
    def merge_period(self):
        self.lighting_periods.sort(key=lambda x:x[0])
        result=[]
        if len(self.lighting_periods)==0:
            return
        
        result.append(self.lighting_periods[0])
        for i in range(1,len(self.lighting_periods)):
            if result[-1][1]>=self.lighting_periods[i][0]:
                result[-1][1]=max(result[-1][1],self.lighting_periods[i][1])
            else:
                result.append(self.lighting_periods[i])
        self.lighting_periods=result
        
    def calculate_time_difference(self,time1, time2):
        # 计算时间差
        time_diff = abs(time1 - time2)
        # 转换为分钟
        time_diff_minutes = time_diff.total_seconds() / 60
        return time_diff_minutes
    
    def calculate_time(self)-> int:
        self.merge_period()
        time=0
        for period in self.lighting_periods:
            time+=self.calculate_time_difference(period[1],period[0])
        return time
        
class LaneSection():
    def __init__(self,id:int,start_x: float,start_y: float,end_x: float,end_y: float,neighbor_ids: List[int]) -> None:
        self.id=id
        # nodes[0] is start node, nodes[-1] is end node
        self.nodes=[Node(start_x,start_y),Node(end_x,end_y)]
        self.neighbor_ids=neighbor_ids
        
    def add_node(self,node:Node):
        self.nodes.insert(-1,node)
        
class Map():
    def __init__(self) -> None:
        self.lane_sections:dict[int,LaneSection]={}
        self.weighted_graph=None

    def add_lane_section(self,lane_section:LaneSection):
        self.lane_sections[lane_section.id]=lane_section

    def get_limit(self)-> Tuple[int,int,int,int]:
        x=list()
        y=list()
        for lane_section_id,lane_section in self.lane_sections.items():
            x.append(lane_section.nodes[0].x)
            y.append(lane_section.nodes[0].y)
            x.append(lane_section.nodes[-1].x)
            y.append(lane_section.nodes[-1].y)
        if len(x)>0:
            xmin=min(x)
            xmax=max(x)
            ymin=min(y)
            ymax=max(y)
        else:
            xmin=0
            xmax=100
            ymin=0
            ymax=100
        return xmin,ymin,xmax,ymax
    
    def get_closest_edge(self,x:float,y:float)-> Tuple[float,Tuple[np.array],float]:
        min_distance=float('inf')
        min_edge_start=None
        min_edge_end=None
        min_proj_point=None
        
        for edge_start,edge_ends in self.weighted_graph.edges.items():
            for edge_end in edge_ends:
                P=(x,y)
                edge_start_node=self.weighted_graph.nodes[edge_start]
                edge_end_node=self.weighted_graph.nodes[edge_end]
                A=(edge_start_node.x,edge_start_node.y)
                B=(edge_end_node.x,edge_end_node.y)
                distance,proj_point=distance2segment(P,A,B)
                
                if distance<min_distance:
                    min_distance=distance
                    min_edge_start_node=edge_start
                    min_edge_end_node=edge_end
                    min_proj_point=proj_point

        return min_edge_start_node,min_edge_end_node,min_distance,min_proj_point
    
    def get_closest_lane_section_id(self,x:float,y:float)-> Tuple[float,Tuple[np.array],float]:
        min_distance=float('inf')
        min_lane_section_id=None
        min_proj_point=None
        for lane_section_id,lane_section in self.lane_sections.items():
            P=(x,y)
            A=(lane_section.nodes[0].x,lane_section.nodes[0].y)
            B=(lane_section.nodes[-1].x,lane_section.nodes[-1].y)
            distance,proj_point=distance2segment(P,A,B)
            if distance<min_distance:
                min_distance=distance
                min_lane_section_id=lane_section_id
                min_proj_point=proj_point
                
        intersection_node=Node(min_proj_point[0],min_proj_point[1])
        return min_lane_section_id,intersection_node,min_distance
    
    
    def connect_sections(self):
        
        pass
    
    def create_weighted_graph_from_lane_sections(self,nodes:List[Node]=None):
        self.weighted_graph=WeightedGraph()
        if not nodes:
            # add the start and end node of the section into weighted graph, and create edge between these two points
            for lane_section_id, lane_section in self.lane_sections.items():
                for node in lane_section.nodes:
                    # self.weighted_graph.add_node(node.id,node)
                    self.weighted_graph.add_node(node)
                for idx in range(len(lane_section.nodes)-1):
                    self.weighted_graph.add_edge(lane_section.nodes[idx].id,lane_section.nodes[idx+1].id)
            # add the edge between the sections
            for lane_section_id, lane_section in self.lane_sections.items():
                for neighbor_id in lane_section.neighbor_ids:
                    neighbor_section=self.lane_sections[neighbor_id]
                    current_node=lane_section.nodes[-1]
                    neighbor_node=neighbor_section.nodes[0]
                    self.weighted_graph.add_edge(current_node.id,neighbor_node.id)

    def get_weighted_graph(self):
        self.create_weighted_graph_from_lane_sections()
        return self.weighted_graph
    
    # insert a new node between two existing nodes
    def insert_node(self,start_node_id,end_node_id,new_node:Node):
        self.weighted_graph.insert_node_in_edge(start_node_id,end_node_id,new_node)
        # if self.weighted_graph.edges
        # self.weighted_graph.add_edge(start_node_id,new_node.id)
        aaaa=1

def main():
    # Path to your CSV file
    csv_file = 'motion_planning/parking_slot.csv'
    read_map(csv_file)

if __name__ == "__main__":
    main()