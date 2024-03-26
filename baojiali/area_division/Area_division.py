# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))
# from Geometric import Polygon
from visualize import visualize
from structure import Parking
from optimizer import optimizer



def main():
    
    parking_counter=[(0, 0), (10, 0), (10, 10), (0,10)]
    
    parking_area=Parking.ParkingArea()
    parking_area.set_counter(parking_counter)
    
    obstacle_countour=[(0,6),(6,6),(6,10),(0,10)]
    parking_area.add_obstacle(obstacle_countour)
    # parking_area.plot()
    # visualize.plot_polygon(parking_area.pos_list)
    
    # min_x=parking_area.get_minX()
    # max_x=parking_area.get_maxX()
    # min_y=parking_area.get_minY()
    # max_y=parking_area.get_maxY()
    
    n=2
    opt=optimizer.AreaOptimizer()
    opt.optimize(division_num=n,parking_area=parking_area)
    
if __name__ == "__main__":
    main()