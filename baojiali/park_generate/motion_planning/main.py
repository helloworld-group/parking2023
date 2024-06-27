from datetime import datetime, timedelta
from implementation import *
from motion_planning.map_tools import*
from park_analysis.park_utils import read_schedule
def generate_path(map:Map,start_location:Node,end_location:Node)->List[Node]:
    weighted_graph=map.create_weighted_graph_from_lane_sections()
    # get the closest edge to start point, insert the proj point into the edge 
    # start_closest_lane_section_id,start_inter_node,start_closesst_distance=map.get_closest_lane_section_id(start_location.x,start_location.y)
    
    # calculate a new node which is the intersection of the closest edge and the start point
    # insert the new node into the map, as the starting node of the path
    min_edge_start,min_edge_end,min_distance,min_proj_point=map.get_closest_edge(start_location.x,start_location.y)
    new_node=Node(min_proj_point[0],min_proj_point[1])
    map.insert_node(min_edge_start,min_edge_end,new_node)
    start_inter_node=new_node
    
    # calculate a new node which is the intersection of the closest edge and the end point
    # insert the new node into the map, as the end node of the path
    min_edge_start,min_edge_end,min_distance,min_proj_point=map.get_closest_edge(end_location.x,end_location.y)
    new_node=Node(min_proj_point[0],min_proj_point[1])
    map.insert_node(min_edge_start,min_edge_end,new_node)
    end_inter_node=new_node
    
    # end_closest_lane_section_id,end_inter_node,end_closesst_distance=map.get_closest_lane_section_id(end_location.x,end_location.y)
    
    # map.lane_sections[start_closest_lane_section_id].add_node(start_inter_node)
    # map.lane_sections[end_closest_lane_section_id].add_node(end_inter_node)
    # # create the weighted graph which contains the end points of each lane section
    # weighted_graph=map.create_weighted_graph_from_lane_sections()
    # map.lane_sections[start_closest_lane_section_id].add_node(start_inter_node)
    # map.lane_sections[end_closest_lane_section_id].add_node(end_inter_node)
    # create the weighted graph which contains the end points of each lane section
    # weighted_graph=map.create_weighted_graph_from_lane_sections()
    # plt.figure(figsize=(10,10))
    # visualize_graph(weighted_graph,'weighted_graph.png')
    # apply A* on the map, to get the path from start point to end point
    came_from, cost_so_far=a_star_search(weighted_graph,start_inter_node,end_inter_node)
    
    # convert the came_from dictionary to a path
    path=convert_to_path(came_from,start_inter_node,end_inter_node)
    return path


def calculate_consumption(lights:Dict[id,Light]):
    total_consumption=0
    total_time=0
    for key,light in lights.items():
        time=light.calculate_time()
        total_time+=time
        # consumption=light.calculate_time()
        total_consumption+=light.calculate_time()
    print("total consumption:",total_consumption)

def main():
    # define map
    map_csv_file='motion_planning/lane_table.csv'
    map=read_lane_map(map_csv_file)
    
    parking_slot_csv_file='motion_planning/parking_slot.csv'
    parking_slots=read_parking_slot(parking_slot_csv_file)

    road_light_csv_file='motion_planning/road_light_table.csv'
    road_lights=read_light(road_light_csv_file)
    
    park_light_csv_file='motion_planning/park_light.csv'
    park_lights=read_light(park_light_csv_file)

    plt.figure(figsize=(10,10))
    visualize_map(map,'lane.png')
    # visualize_graph(map.get_weighted_graph(),'weighted_graph.png')
    visualize_parking_slots(map,parking_slots,'parking_slot.png')
    
    parking_entrance=map.lane_sections[0].nodes[0]
    entrance_schedule_file='motion_planning/entrance_schedule.csv'
    entrance_schedules=read_schedule(entrance_schedule_file)
    # set the motion planning start node and end node
    parking_entrance=map.lane_sections[0].nodes[0]
    
    for idx,schedule in entrance_schedules.items():
        start_location=parking_entrance
        target_park_slot=parking_slots[schedule.target_id]
        
        # calculate the path with A* from start to end
        path=generate_path(map,start_location,target_park_slot)
        
        # calculate the lights which are activate by the path
        road_lights=schedule.calculate_light_periods(schedule.start_time,path,road_lights)
        # calculate the park light activated by the target parking slotgit
        park_lights=schedule.calculate_park_light_periods(target_park_slot,schedule.start_time,park_lights)
    #     park_lights=1
    print('road light consumption:',sep='')
    calculate_consumption(road_lights)
    print('park light consumption:',sep='')
    calculate_consumption(park_lights)
    
    start_location=parking_entrance
    end_location=parking_slots[36]
    
    # calculate the path with A* from start to end
    path=generate_path(map,start_location,end_location)
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