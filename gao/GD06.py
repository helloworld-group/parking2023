import matplotlib.pyplot as plt

class site_rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width


class obstacle:
    def __init__(self, length, width, x, y):
        self.length = length
        self.width = width
        self.position = (x, y)


#障碍物子类 柱
class core(obstacle):
    pass

#障碍物子类 核心筒
class column(obstacle):
    pass

#障碍物子类 不可行域
class forbidden_region(obstacle):
    pass

def create_adjustable_grid(rows, cols, spacing):
    fig, ax = plt.subplots()

    # 绘制水平线
    for i in range(rows + 1):
        ax.axhline(i * spacing, color='black', linewidth=1)

    # 绘制垂直线
    for j in range(cols + 1):
        ax.axvline(j * spacing, color='black', linewidth=1)

    ax.set_xticks([i * spacing for i in range(cols + 1)])
    ax.set_yticks([i * spacing for i in range(rows + 1)])

import matplotlib.patches as patches

def create_filled_grid(rows, cols, spacing, filled_rectangles):
    fig, ax = plt.subplots()

    # 绘制水平线
    for i in range(rows + 1):
        ax.axhline(i * spacing, color='blue', linewidth=1)

    # 绘制垂直线
    for j in range(cols + 1):
        ax.axvline(j * spacing, color='orange', linewidth=1)

    ax.set_xticks([i * spacing for i in range(cols + 1)])
    ax.set_yticks([i * spacing for i in range(rows + 1)])

    # 添加填充障碍物
    for rect_position in filled_rectangles:
        rect = patches.Rectangle((rect_position[0] * spacing, rect_position[1] * spacing),
                                 spacing, spacing, linewidth=1, edgecolor='none', facecolor='gray')
        ax.add_patch(rect)

    # 设置图表标题
    plt.title("Site Plan")

    # 设置坐标轴标题
    ax.set_xlabel("Length")
    ax.set_ylabel("Width")

    plt.grid()
    plt.show()

# 例子：创建一个矩形停车场平面网格，间距为20，填充障碍空间
create_filled_grid(10, 10, 20, [(8, 2), (3, 4), (4, 0), (4, 1)])
