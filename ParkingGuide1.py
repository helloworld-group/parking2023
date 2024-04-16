import heapq
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Node:
    def __init__(self, x, y, cost=float('inf')):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = 0
        self.parent = None


    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic

class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def heuristic(self, current, goal):
        return abs(current.x - goal.x) + abs(current.y - goal.y)

    def neighbors(self, node):
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Four directions: right, left, down, up
        for dx, dy in directions:
            x, y = node.x + dx, node.y + dy
            if 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != 1:
                neighbors.append(Node(x, y))
        return neighbors

    def find_path(self, start, goal):
        start_node = Node(start[0], start[1], 0)
        goal_node = Node(goal[0], goal[1])
        start_node.heuristic = self.heuristic(start_node, goal_node)

        frontier = []
        heapq.heappush(frontier, start_node)
        visited = set()
        path_length = 0

        while frontier:
            current = heapq.heappop(frontier)
            if (current.x, current.y) == (goal_node.x, goal_node.y):
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                path_length = len(path) - 1  # 计算路径长度（减去起点）
                return path[::-1], path_length  # 返回路径和长度

            visited.add((current.x, current.y))

            for neighbor in self.neighbors(current):
                if (neighbor.x, neighbor.y) not in visited:
                    neighbor_cost = current.cost + 1  # 计算邻居节点的代价
                    if neighbor.cost > neighbor_cost:
                        neighbor.cost = neighbor_cost
                        neighbor.heuristic = self.heuristic(neighbor, goal_node)
                        neighbor.parent = current
                        heapq.heappush(frontier, neighbor)

        return None, None  # 如果未找到路径，返回空值

def visualize_map(grid_map, path):
    cmap = ListedColormap(['blue', 'red', 'green', 'yellow', 'purple'])
    plt.figure(figsize=(8, 8))
    plt.imshow(grid_map, cmap=cmap, origin='lower')

    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='purple', marker='o')

    plt.xticks(range(len(grid_map)))
    plt.yticks(range(len(grid_map)))
    plt.grid(True)
    plt.title('A* Pathfinding Visualization')
    plt.show()

# Example usage
grid_map = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

astar = AStar(grid_map)
start_point = (1, 0)
end_point = (4, 4)
path, path_length = astar.find_path(start_point, end_point)
print("Path:", path)
print("Path Length:", path_length)
visualize_map(grid_map, path)