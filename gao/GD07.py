import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Line:
    pass

class Site:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')

class Depot:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Obstacle:
    pass

class Column(Obstacle):
    pass

class Core(Obstacle):
    pass

# 创建 Site 实例
site_plan = Site(3000, 2000)

# 创建 Depot 实例
depot = Depot(100, 100, 300, 200)

# 绘制网格，间隔为100米
for i in range(0, site_plan.width + 1, 100):
    site_plan.ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
    site_plan.ax.axhline(i, color='gray', linestyle='--', linewidth=0.5)
    # 设置图表标题
    plt.title("Site Plan")

# 在 site plan 矩形中绘制4个小矩形，填充为灰色
rectangles = [
    patches.Rectangle((0, 0), 500, 1000, linewidth=1, edgecolor='black', facecolor='gray'),
    patches.Rectangle((800, 600), 200, 150, linewidth=1, edgecolor='black', facecolor='gray'),
    patches.Rectangle((1200, 800), 300, 200, linewidth=1, edgecolor='black', facecolor='gray'),
    patches.Rectangle((400, 1200), 500, 400, linewidth=1, edgecolor='black', facecolor='gray')
]

for rect in rectangles:
    site_plan.ax.add_patch(rect)

# 显示绘图
plt.show()
