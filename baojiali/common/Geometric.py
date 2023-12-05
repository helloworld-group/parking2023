
class Polygon:
    def __init__(self) -> None:
        self.pos_list=[]
        pass
    
    def add_point_list(self,pos_list):
        for pos in pos_list:
            self.pos_list.append(pos)
        pass
    
    def get_minX(self):
        x_values, y_values = zip(*self.pos_list)
        return min(x_values)
    
    def get_maxX(self):
        x_values, y_values = zip(*self.pos_list)
        return max(x_values)
    
    def get_minY(self):
        x_values, y_values = zip(*self.pos_list)
        return min(y_values)
    
    def get_maxY(self):
        x_values, y_values = zip(*self.pos_list)
        return max(y_values)

def main():
    polygon=Polygon()
    pos_list=[]
    pos_list.append((0,0))
    pos_list.append((10,0))
    pos_list.append((10,5))
    pos_list.append((5,5))
    polygon.add_point_list(pos_list)
if __name__ == "__main__":
    main()