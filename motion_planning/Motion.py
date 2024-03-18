from Map import GridMap
from collections import deque


def Dijkstra(gridmap,start,goal):
    """_summary_

    Args:
        gridmap (_type_): _description_
        start (_type_): _description_
        goal (_type_): _description_
    """
    pass

def Astart(gridmap,start,goal):
    """_summary_

    Args:
        gridmap (_type_): _description_
        start (_type_): _description_
        goal (_type_): _description_
    """
    pass

def BFS(gridmap,start,goal):
    """_summary_

    Args:
        gridmap (int[][]): _description_
        start (int[][]): _description_
        goal (int[][]): _description_
    """
    came_from={}
    frontier=deque()
    frontier.append(start)
    while frontier:
        current=frontier.popleft()
        if current == goal: 
            break  
        for next in gridmap.neighbors(current[0],current[1]):
            key_next = tuple(next)
            if key_next not in came_from.keys():
                frontier.append(next)
                came_from[key_next] = current
    
    current = goal 
    path = []
    while current != start: 
        path.append(current)
        key_current=tuple(current)
        current = came_from[key_current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def main():
    width=20
    height=20
    map=GridMap(width,height)
    map.add_obstacle(row=2,col=2,width=4,height=4)
    map.print()
    start=[3,0]
    goal=[3,6]
    path=BFS(map,start,goal)
    print(path)
    # map.plot()
    pass

if __name__ == '__main__':
    main()