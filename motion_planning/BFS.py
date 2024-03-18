from Map import GridMap


def BFS(gridmap,start,end):
    
    pass

def main():

    width=20
    height=20
    map=GridMap(width,height)
    map.add_obstacle(row=2,col=2,width=4,height=4)
    map.print()
    pass

if __name__ == '__main__':
    main()