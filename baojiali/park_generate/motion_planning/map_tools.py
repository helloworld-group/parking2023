import csv
from motion_planning.implementation import WeightedGraph,Location
import matplotlib.pyplot as plt
from typing import List,Dict,Tuple,Optional
# csv_file:Path to your CSV file
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
                location=Location(id_,x_coord,y_coord)
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
                    
                aaa=1
                    
                

    # Print or use the data as needed
    print("IDs:", ids)
    print("X coordinates:", x_coords)
    print("Y coordinates:", y_coords)
    print("Neighbors:", neighbors)
    return graph

def visualize_map(map:WeightedGraph,img_name=None):
    
    plt.figure()
    # plot all the nodes
    for id,location in map.nodes.items():
        plt.scatter(location.x,location.y,color='red',marker='o')
    
        # break
    
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
    plt.xlim(xmin-5,xmax+5)
    plt.ylim(ymin-5,ymax+5)
    if img_name:
        plt.savefig(img_name,format='png',dpi=100)
    # plt.legend()



def visualize_path(map,path:Dict[Location, Optional[Location]],start_location:Location,end_location:Location):
    
    visualize_map(map)
    # plt.figure()
    # xmin,ymin,xmax,ymax=map.get_limit()
    # plt.xlim(xmin-5,xmax+5)
    current_location=end_location
    while current_location!=start_location:
        # print(current)
        prev_location=path[current_location]
        # print(next_location)
        # plt.plot([current.x,prev_location.x],[current.y,prev_location.y],color='blue')
        
        point1=(current_location.x,current_location.y)
        point2=(prev_location.x,prev_location.y)
        plt.annotate('', xy=point1, xycoords='data', xytext=point2, textcoords='data',arrowprops=dict(arrowstyle="->",color='red',lw=2))
        current_location=prev_location
    pass

def main():
    # Path to your CSV file
    csv_file = 'motion_planning/parking_slot.csv'
    read_map(csv_file)

if __name__ == "__main__":
    main()