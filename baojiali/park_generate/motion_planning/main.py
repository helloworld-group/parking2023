from datetime import datetime, timedelta
from implementation import *
from motion_planning.map_tools import*
from park_analysis.park_utils import read_schedule
import copy
def position_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
    

def proj_parkslot_on_graph(weighted_graph:WeightedGraph,parking_slot: ParkingSlot)->Node:
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
    edge_start_id,edge_end_id,min_distance,min_proj_point=map.get_closest_edge(parking_slot.x,parking_slot.y)
    # if the new node is very close to the end of the edge, do not insert

    edge_start_node=map.weighted_graph.nodes[edge_start_id]
    edge_end_node=map.weighted_graph.nodes[edge_end_id]
    if position_distance(min_proj_point[0],min_proj_point[1],edge_start_node.x,edge_start_node.y)<0.1:
        proj_node=edge_start_node   
    elif position_distance(min_proj_point[0],min_proj_point[1],edge_end_node.x,edge_end_node.y)<0.1:
        proj_node=edge_end_node
    else:
        new_node=Node(min_proj_point[0],min_proj_point[1])
        map.insert_node(edge_start_id,edge_end_id,new_node)
        proj_node=new_node
    return proj_node
    
    
def generate_pedestrian_path(weighted_graph: WeightedGraph,start_location:ParkingSlot,end_location:ParkingSlot)->List[Node]:
    start_node=proj_parkslot_on_graph(weighted_graph,start_location)
    end_node=proj_parkslot_on_graph(weighted_graph,end_location)
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

def main():
    # define map
    
    idx=3
    map_csv_file='motion_planning/lane_table_map_'+str(idx)+'.csv'
    map=read_lane_map(map_csv_file)
    pedestrian_map_csv_file='motion_planning/pedestrian_graph_'+str(idx)+'.csv'
    map_pedestrian=read_pedestrian_map(pedestrian_map_csv_file)
    # map_pedestrian.lane_sections=[]
    parking_slot_csv_file='motion_planning/parking_slot_'+str(idx)+'.csv'
    parking_slots=read_parking_slot(parking_slot_csv_file)

    entrances,exits=read_entrance_exit(parking_slot_csv_file)

    road_light_csv_file='motion_planning/road_light_'+str(idx)+'.csv'
    road_lights=read_light(road_light_csv_file)
    
    park_light_csv_file='motion_planning/park_light_'+str(idx)+'.csv'
    park_lights=read_light(park_light_csv_file)

    plot_text=True
    plt.figure(figsize=(10,10))
    # visualize_light(road_lights,color='blue')
    # visualize_light(park_lights,color='blue')
    # visualize_map(map,'lane.png',plot_text=plot_text)
    visualize_graph(map_pedestrian.weighted_graph,'pedestrian_graph.png',plot_text=plot_text)
    visualize_graph(map.get_weighted_graph(),'weighted_graph.png',plot_text=plot_text)
    # visualize_parking_slots(map,parking_slots,slot_color='slategrey',img_name='parking_slot.png',plot_text=plot_text)
    # visualize_parking_slots(map,entrances,slot_color='crimson',img_name='parking_slot.png',s=200,marker='*',plot_text=plot_text)
    # visualize_parking_slots(map,exits,slot_color='limegreen',img_name='parking_slot.png',s=200,marker='*',plot_text=plot_text)
    vehicle_schedule_file='motion_planning/peak_data/entrance_booking_schedule_'+str(idx)+'.csv'
    # vehicle_schedule_file='motion_planning/entrance_booking_schedule_'+str(idx)+'.csv'

    vehicle_schedules=read_schedule(vehicle_schedule_file)
    # set the motion planning start node and end node
    parking_entrance=map.lane_sections[0].nodes[0]
    
    for idx,schedule in vehicle_schedules.items():
        print(idx)
        # if idx==148:
        #     aaaa=1
        #     continue
        entrance_park_slot=entrances[schedule.entrance_id]
        target_park_slot=parking_slots[schedule.target_id]
        exit_part_slot=exits[schedule.exit_id]
        # calculate the 
        # path with A* from start to end
        map.create_weighted_graph_from_lane_sections()
        map_pedestrian=read_pedestrian_map(pedestrian_map_csv_file)
        # print('vehicle path:',end='')
        path_vehicle=generate_path(map,entrance_park_slot,target_park_slot)
        # for node in path_vehicle:
        #     print(node.id,end=',')
        path_pedestrian=generate_pedestrian_path(map_pedestrian.weighted_graph,target_park_slot,exit_part_slot)
        
        # print(" ")
        # print('pedestrian path:',end='')
        # for node in path_pedestrian:
        #     print(node.id,end=',')
        # plt.figure(figsize=(10,10))
        # visualize_parking_slots(map,parking_slots)
        # visualize_light(road_lights)
        # visualize_light(park_lights,color='cyan')
        # visualize_map(map,'map.png')
        # visualize_path(map,path_vehicle,path_color='firebrick',img_name='path.png')
        # visualize_path(map,path_pedestrian,path_color='darkorange',img_name='path.png')

        # calculate the lights which are activate by the path
        road_lights=schedule.calculate_light_periods(schedule.start_time,path_vehicle,road_lights)
        # calculate the park light activated by the target parking slotgit
        park_lights=schedule.calculate_park_light_periods(target_park_slot,schedule.start_time,park_lights)
 
        road_lights=schedule.calculate_light_periods(schedule.start_time,path_pedestrian,road_lights)
    
    
    
    #     park_lights=1
    
    print('road light consumption by vehicle:',end='')
    calculate_consumption(road_lights)
    print('park light consumption:',end='')
    calculate_consumption(park_lights)
    
    # path generation testing sample
    start_location=parking_entrance
    end_location=parking_slots[36]
    
    # calculate the path with A* from start to end
    # path=generate_path(map,start_location,end_location)
    # calculate the lights which are activate by the path
    
    
    # # plot map
    plt.figure(figsize=(10,10))
    visualize_parking_slots(map,parking_slots)
    visualize_light(road_lights)
    visualize_light(park_lights,color='cyan')
    visualize_map(map)

    visualize_path(map,path,'path.png')


if __name__ == "__main__":
    main()