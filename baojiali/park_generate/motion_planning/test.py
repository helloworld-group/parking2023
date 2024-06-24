from implementation import *
from motion_planning.map_tools import read_map,visualize_map,visualize_path



# def breadth_first_search(graph: Graph, start: Location, goal: Location):
#     frontier = Queue()
#     frontier.put(start)
#     came_from: dict[Location, Optional[Location]] = {}
#     came_from[start] = None
    
#     while not frontier.empty():
#         current: Location = frontier.get()
        
#         if current == goal: # early exit
#             break
        
#         for next in graph.neighbors(current):
#             if next not in came_from:
#                 frontier.put(next)
#                 came_from[next] = current
    
#     return came_from

# g = SquareGrid(30, 15)
# g.walls = DIAGRAM1_WALLS

# start = (8, 7)
# goal = (17, 2)
# parents = breadth_first_search(g, start, goal)
# draw_grid(g, point_to=parents, start=start, goal=goal)

def main():
    # define map
    csv_file = 'motion_planning/parking_slot.csv'
    map=read_map(csv_file)
    visualize_map(map,'map.png')
    
    
    # apply A* on the map, to get the path from start point to end point
    
    
    # plot the path
    
    start_location=map.get_location(1)
    end_location=map.get_location(5)
    
    came_from, cost_so_far=a_star_search(map,start_location,end_location)
    # plot map
    
    visualize_path(map,came_from,start_location,end_location)
    
    pass

if __name__ == "__main__":
    main()