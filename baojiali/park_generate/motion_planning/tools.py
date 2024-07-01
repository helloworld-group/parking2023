from motion_planning.map import *
from motion_planning.graph import *


def position_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
    

def proj_parkslot_graph(weighted_graph:WeightedGraph,parking_slot: ParkingSlot)->Node:
    edge_start_id,edge_end_id,min_distance,min_proj_point=weighted_graph.get_closest_edge(parking_slot.x,parking_slot.y)
    # if the new node is very close to the end of the edge, do not insert

    edge_start_node=weighted_graph.nodes[edge_start_id]
    edge_end_node=weighted_graph.nodes[edge_end_id]
    if position_distance(min_proj_point[0],min_proj_point[1],edge_start_node.x,edge_start_node.y)<0.1:
        proj_node=edge_start_node   
    elif position_distance(min_proj_point[0],min_proj_point[1],edge_end_node.x,edge_end_node.y)<0.1:
        proj_node=edge_end_node
    else:
        new_node=Node(min_proj_point[0],min_proj_point[1])
        weighted_graph.insert_node_in_edge(edge_start_id,edge_end_id,new_node)
        proj_node=new_node
    return proj_node


def proj_parkslot_on_map(map:Map,parking_slot:ParkingSlot)->Node:
    proj_node=proj_parkslot_graph(map.weighted_graph,parking_slot)
    return proj_node

    
    
def generate_pedestrian_path(weighted_graph: WeightedGraph,start_location:ParkingSlot,end_location:ParkingSlot)->List[Node]:
    start_node=proj_parkslot_graph(weighted_graph,start_location)
    end_node=proj_parkslot_graph(weighted_graph,end_location)
    # plt.figure(figsize=(10,10))
    
    # visualize_graph(weighted_graph,'pedestrian_weighted_graph_inserted.png')
    # apply A* on the map, to get the path from start point to end point
    came_from, cost_so_far=a_star_search(weighted_graph,start_node,end_node)
    
    # convert the came_from dictionary to a path
    path=convert_to_path(came_from,start_node,end_node)
    return path

def generate_path(map:Map,start_location:ParkingSlot,end_location:ParkingSlot)->List[Node]:
    # weighted_graph=map.create_weighted_graph_from_lane_sections()

    start_node=proj_parkslot_on_map(map,start_location)
    end_node=proj_parkslot_on_map(map,end_location)
    # plt.figure(figsize=(10,10))
    
    # visualize_graph(map.weighted_graph,'weighted_graph_inserted.png')
    # apply A* on the map, to get the path from start point to end point
    came_from, cost_so_far=a_star_search(map.weighted_graph,start_node,end_node)
    
    # convert the came_from dictionary to a path
    path=convert_to_path(came_from,start_node,end_node)
    return path


def calculate_consumption(lights:Dict[id,Light]):
    total_consumption=0
    total_time=0
    for key,light in lights.items():
        time=light.calculate_time()
        total_time+=time
        # consumption=light.calculate_time()
        total_consumption+=light.calculate_time()
    print("total minutes:",total_consumption)

def visualize_full_path():
    aaaa=1
    
    
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
    """连接两个道路section，返回两个连接的点"""
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
    """将came_from转换为路径"""
    current_location=end_location
    inverse_path=[]
    while current_location!=start_location:
        inverse_path.append(current_location)
        prev_location=came_from[current_location]
        current_location=prev_location
    inverse_path.append(start_location)
    path=inverse_path[::-1]
    return path