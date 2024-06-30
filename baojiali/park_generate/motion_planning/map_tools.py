import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List,Dict,Tuple,Optional
from datetime import datetime
from motion_planning.implementation import WeightedGraph,Node
from math_tool import point_to_segment_distance_with_intersection
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
        distance,proj_point=point_to_segment_distance_with_intersection(P,A,B)
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
                distance,proj_point=point_to_segment_distance_with_intersection(P,A,B)
                
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
            distance,proj_point=point_to_segment_distance_with_intersection(P,A,B)
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


def read_light(csv_file:str)->Dict[int,Light]:
    lights:Dict[int,Light]={}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if exists
        for row in reader:
            id = int(row[0])
            x= float(row[1])
            y= float(row[2])
            light=Light(id,x,y)
            lights[id]=light
    return lights

def read_entrance_exit(csv_file: str):
    entrances:Dict[int,ParkingSlot]={}
    exits:Dict[int,ParkingSlot]={}
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        id = int(row['id'])
        x= float(row['x'])
        y = float(row['y'])
        if row['type']=='entrance':
            entrance=ParkingSlot(id,x,y)
            entrances[id]=entrance
        elif row['type']=='exit':
            exit=ParkingSlot(id,x,y)
            exits[id]=exit

    return entrances,exits



def read_parking_slot(csv_file: str):
    parking_slots:Dict[int,ParkingSlot]={}
    
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        id = int(row['id'])
        x= float(row['x'])
        y = float(row['y'])
        if pd.isna(row['type']):
            parking_slot=ParkingSlot(id,x,y)
            parking_slots[id]=parking_slot
    return parking_slots


def read_pedestrian_map(csv_file:str)->Map:
    map=Map()
    map.weighted_graph=WeightedGraph()
    
    df = pd.read_csv(csv_file)
    # 遍历每一行
    for index, row in df.iterrows():
        id = int(row['node_id'])
        x= float(row['x'])
        y = float(row['y'])
        neighbor_ids=[]
        if not pd.isna(row['neibor_ids']):
            neighbor_ids_str = str(row['neibor_ids']).strip('"')
            if neighbor_ids_str:
                neighbor_ids = [int(n_id) for n_id in neighbor_ids_str.split(',')]
        node=Node(x,y,id)
        map.weighted_graph.add_node(node)
        for neighbor_id in neighbor_ids:
            map.weighted_graph.add_edge(id,neighbor_id)
    return map
        
        # lane_section=LaneSection(id,start_x,start_y,end_x,end_y,neighbor_ids)
        # map.add_lane_section(lane_section)


def read_lane_map(csv_file:str)->Map:
    # Read data from CSV file
    map=Map()
    
    df = pd.read_csv(csv_file)
    # 遍历每一行
    for index, row in df.iterrows():
        id = int(row['lane_id'])
        start_x= float(row['start_x'])
        start_y = float(row['start_y'])
        end_x= float(row['end_x'])
        end_y= float(row['end_y'])
        neighbor_ids=[]
        if not pd.isna(row['neibor_ids']):
            neighbor_ids_str = str(row['neibor_ids']).strip('"')
            if neighbor_ids_str:
                neighbor_ids = [int(n_id) for n_id in neighbor_ids_str.split(',')]
        lane_section=LaneSection(id,start_x,start_y,end_x,end_y,neighbor_ids)
        map.add_lane_section(lane_section)
    
    return map
    
    
def read_map(csv_file:str)->WeightedGraph:
    # there are 4 columns in the csv file, which are node ID, nodeX, nodeY, neighbors
    graph=WeightedGraph()
    ids = []
    x_coords = []
    y_coords = []
    neighbors = {}

    # Read data from CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # next(reader)  # Skip header row if exists
        for row in reader:
            if len(row) == 4:
                # Extract data from columns
                id_ = int(row[0])
                x_coord = float(row[1])
                y_coord = float(row[2])
                
                # add the node into weighted graph
                location=Node(id_,x_coord,y_coord)
                graph.add_node(id_,location)
                
                neighbor_ids_str = row[3].strip('"')  # Remove surrounding quotes if any
                # Store in lists
                ids.append(id_)
                x_coords.append(x_coord)
                y_coords.append(y_coord)
                
                # Process neighbors
                if neighbor_ids_str:
                    neighbor_ids = [int(n_id) for n_id in neighbor_ids_str.split(',')]
                    neighbors[id_] = neighbor_ids
                    for neighbor_id in neighbor_ids:
                        graph.add_edge(id_,neighbor_id)
                else:
                    neighbors[id_] = []

    return graph


# calculate the distance between two lane section, and return the connected end node
def get_connection(lane0:LaneSection,lane1:LaneSection)-> Tuple[Node,Node]:
    min_distance=float('inf')
    result_node0=None
    result_node1=None
    for node0 in lane0.nodes:
        for node1 in lane1.nodes:
            distance=math.sqrt((node0.x-node1.x)**2+(node0.y-node1.y)**2)
            if(distance<min_distance):
                min_distance=distance
                result_node0=node0
                result_node1=node1

    return (result_node0,result_node1)
    

def visualize_light(lights:Dict[int,Light],color='blue',img_name=None):
    for light_id,light in lights.items():
        plt.scatter(light.x,light.y,color=color,marker='o')

    
def visualize_map(map: Map,img_name=None,node_color='coral',plot_text=True):
    
    xmin,ymin,xmax,ymax=map.get_limit()
    plt.xlim(xmin-20,xmax+20)
    plt.ylim(ymin-20,ymax+20)
    for id,lane_section in map.lane_sections.items():
        # plot the start node and end node, and draw the arrow between them
        plt.scatter(lane_section.nodes[0].x,lane_section.nodes[0].y,color=node_color,marker='o')
        plt.scatter(lane_section.nodes[-1].x,lane_section.nodes[-1].y,color=node_color,marker='o')
        
        middle_x=(lane_section.nodes[0].x+lane_section.nodes[-1].x)/2
        middle_y= (lane_section.nodes[0].y+lane_section.nodes[-1].y)/2
        if plot_text:
            plt.text(middle_x+0.5, middle_y + 0.5, f'lane:{lane_section.id}', fontsize=8, ha='center', color='black')
        # draw arrow from start node to end node
        point1=(lane_section.nodes[0].x,lane_section.nodes[0].y)
        point2=(lane_section.nodes[-1].x,lane_section.nodes[-1].y)
        # note, xytext is the start point, and xy is the end point
        plt.annotate('', xy=point2, xycoords='data', xytext=point1, textcoords='data',arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=0"))
        
        # plot the arrow to the neighbors
        for neighbor_id in lane_section.neighbor_ids:
            if neighbor_id in map.lane_sections.keys():
                neighbor_section=map.lane_sections[neighbor_id]
                # # get the closest end in current lane and neighbor end, which will be connected
                # current_end,neighbor_end=get_connection(lane_section,neighbor_section)
                # neighbor_section.nodes[0]
                point1=(lane_section.nodes[-1].x,lane_section.nodes[-1].y)
                point2=(neighbor_section.nodes[0].x,neighbor_section.nodes[0].y)
                # note, xytext is the start point, and xy is the end point
                plt.annotate('', xy=point2, xycoords='data', xytext=point1, textcoords='data',arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=0",color='green'))
        
        
        
    if img_name:
        plt.savefig(img_name,format='png',dpi=100)
    # plt.show()

def visualize_parking_slots(map: Map,parking_slots: Dict[int,ParkingSlot],slot_color='cyan',marker='o',img_name=None,s=40,plot_text=True):
    for id,parking_slot in parking_slots.items():
        plt.scatter(parking_slot.x,parking_slot.y,color=slot_color,marker=marker,s=s)
        if plot_text:
            plt.text(parking_slot.x+1, parking_slot.y + 0.5, f'{parking_slot.id}', fontsize=8, ha='center', color='black')
        
    if img_name:
        plt.savefig(img_name,format='png',dpi=100)


def visualize_graph(map:WeightedGraph,img_name=None,node_color='coral',plot_text=True):
    for id,location in map.nodes.items():
        plt.scatter(location.x,location.y,color=node_color,marker='o')
        if plot_text:
            plt.text(location.x+1, location.y + 0.5, f'{location.id}', fontsize=8, ha='center', color='black')
    
    # plot all the edges
    for node_id,neighbor_list in map.edges.items():
        for neighbor_id in neighbor_list:
            node_location=map.nodes[node_id]
            neighbor_location=map.nodes[neighbor_id]
            point1=(neighbor_location.x,neighbor_location.y)
            point2=(node_location.x,node_location.y)
            # note, xytext is the start point, and xy is the end point
            plt.annotate('', xy=point1, xycoords='data', xytext=point2, textcoords='data',arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=0"))
    
    
    plt.gca().set_aspect('equal')
    xmin,ymin,xmax,ymax=map.get_limit()
    plt.xlim(xmin-20,xmax+20)
    plt.ylim(ymin-20,ymax+20)
    if img_name:
        plt.savefig(img_name,format='png',dpi=100)
    # plt.legend()


# convert came_from to the path
def convert_to_path(came_from:Dict[Node, Optional[Node]],start_location:Node,end_location:Node)-> List[Node]:
    current_location=end_location
    inverse_path=[]
    while current_location!=start_location:
        inverse_path.append(current_location)
        prev_location=came_from[current_location]
        current_location=prev_location
    inverse_path.append(start_location)
    path=inverse_path[::-1]
    return path

def visualize_path(map,path,path_color='red',img_name=None):
    # current_location=end_location
    
    # path=convert_to_path(came_from,start_location,end_location)
    
    for idx_node in range(len(path)-1):
        point1=(path[idx_node].x,path[idx_node].y)
        point2=(path[idx_node+1].x,path[idx_node+1].y)
        # note, xytext is the start point, and xy is the end point
        plt.annotate('', xy=point2, xycoords='data', xytext=point1, textcoords='data',arrowprops=dict(arrowstyle="->",color=path_color,lw=2))
        
    plt.scatter(path[0].x,path[0].y,color='magenta',marker="*",linewidths=5)
    plt.scatter(path[-1].x,path[-1].y,color='lime',marker="*",linewidths=5)
    
    if img_name:
        plt.savefig(img_name,format='png',dpi=100)
        print("result saved in to:"+img_name)
    # print(path[:-1])

def main():
    # Path to your CSV file
    csv_file = 'motion_planning/parking_slot.csv'
    read_map(csv_file)

if __name__ == "__main__":
    main()