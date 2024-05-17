
class VPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VEdge:
    def __init__(self, start: VPoint, end: VPoint, cost):
        self.start = start
        self.end = end
        self.cost = cost

    def __str__(self) -> str:
        return f"({self.start.x},{self.start.y}) -> ({self.end.x},{self.end.y})"

class VGraph:
    def __init__(self):
        self.points = []
        self.edges = []

    def add_point(self, point: VPoint):
        self.points.append(point)

    def add_edge(self, edge: VEdge):
        self.edges.append(edge)

    def is_point_in_graph(self, point: VPoint):
        for i, p in enumerate(self.points):
            # if abs(p.x - point.x) < CFG.eps and abs(p.y - point.y) < CFG.eps:
            if abs(p.x - point.x) < 1e-6 and abs(p.y - point.y) < 1e-6:
                return True
        return False

def from_rectangle_to_graph(polygon_bounds):
    graph = VGraph()
    for polygon_bound in polygon_bounds:
        minx, miny, maxx, maxy = polygon_bound
        point_list = []
        point_list.append(VPoint(minx, miny))
        point_list.append(VPoint(minx, maxy))
        point_list.append(VPoint(maxx, miny))
        point_list.append(VPoint(maxx, maxy))
        for point in point_list:
            if not graph.is_point_in_graph(point):
                graph.add_point(point)
        edge_list = []
        edge_list.append(
            VEdge(
                point_list[0],
                point_list[1],
                abs(point_list[0].x - point_list[1].x),
            )
        )
        edge_list.append(
            VEdge(
                point_list[1],
                point_list[2],
                abs(point_list[1].y - point_list[2].y),
            )
        )
        edge_list.append(
            VEdge(
                point_list[2],
                point_list[3],
                abs(point_list[2].x - point_list[3].x),
            )
        )
        edge_list.append(
            VEdge(
                point_list[3],
                point_list[0],
                abs(point_list[3].y - point_list[0].y),
            )
        )
        for edge in edge_list:
            graph.add_edge(edge)
    return graph