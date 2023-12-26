from common import Geometric
from visualize import visualize
class ParkingArea():
    def __init__(self) -> None:
        super().__init__()
        self.countour=Geometric.Polygon()
        self.obstacles=[]
        
    def set_counter(self,pos_list:[]):
        self.countour.add_point_list(pos_list)
        pass
    
    def get_maxX(self):
        return self.countour.get_maxX()
    
    def get_minX(self):
        return self.countour.get_minX()
    
    def get_maxY(self):
        return self.countour.get_maxY()

    def get_minY(self):
        return self.countour.get_minY()
    
    def add_obstacle(self,pos):
        obstacle=Geometric.Polygon()
        obstacle.add_point_list(pos)
        self.obstacles.append(obstacle)
        pass
    
    def plot(self):
        # plot countour
        visualize.plot_polygon(self.countour.pos_list)
        
        # plot obstacle
        for obstacle in self.obstacles:
            visualize.plot_polygon(obstacle.pos_list,fill_color='gray')
        pass
    