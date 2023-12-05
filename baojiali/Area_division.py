# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

# from Geometric import Polygon
from common import Geometric

class ParkingArea(Geometric.Polygon):
    def __init__(self) -> None:
        super().__init__()
        aaa=1
    pass

def main():
    
    pos_list=[]
    pos_list.append((0,0))
    pos_list.append((10,0))
    pos_list.append((10,5))
    pos_list.append((5,5))
    
    parking_area=ParkingArea()
    parking_area.add_point_list(pos_list)
    min_x=parking_area.get_minX()
    aaa=1
if __name__ == "__main__":
    main()