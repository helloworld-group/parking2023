import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class 车位:
    def __init__(self, 长度, 宽度, 方向, 位置):
        self.长度 = 长度
        self.宽度 = 宽度
        self.方向 = 方向
        self.位置 = 位置

class 柱:
    def __init__(self, 长度, 宽度, 位置):
        self.长度 = 长度
        self.宽度 = 宽度
        self.位置 = 位置

class 核心筒:
    def __init__(self, 长度, 宽度, 位置):
        self.长度 = 长度
        self.宽度 = 宽度
        self.位置 = 位置

class 车道:
    def __init__(self, 宽度, 中心定位点):
        self.宽度 = 宽度
        self.中心定位点 = 中心定位点

class 车库:
    def __init__(self, 长度, 宽度, 位置):
        self.长度 = 长度
        self.宽度 = 宽度
        self.位置 = 位置

class 内轮廓:
    def __init__(self, 长度, 宽度):
        self.长度 = 长度
        self.宽度 = 宽度

# 创建一个空的图形对象
fig, ax = plt.subplots()

# 创建类的实例
内轮廓实例 = 内轮廓(120, 60)
车位列表 = []
车位数量 = 220
车位长度 = 5.4
车位宽度 = 2.4
柱子宽度 = 0.5
柱子长度 = 0.5
核心筒长度 = 10
核心筒宽度 = 10
车道宽度 = 6
每组车位数 = 3
车道长度=内轮廓实例.长度-车位宽度*每组车位数

# 每组车位数量为3，每组车位后有一个柱子
每行组数 = 内轮廓实例.长度 // (每组车位数 * 车位宽度 + 柱子宽度)

# 计算核心筒占用的位置范围
核心筒位置x = (内轮廓实例.长度 - 核心筒长度) / 2
核心筒位置y = (内轮廓实例.宽度 - 核心筒宽度) / 2
核心筒左上角 = (核心筒位置x, 核心筒位置y)
核心筒右下角 = (核心筒位置x + 核心筒长度, 核心筒位置y + 核心筒宽度)

# 单行车位的Y轴起始位置
y_offset = 车位长度+车道宽度
# 单行车位的X轴起始位置
x_offset = 车位长度+车道宽度

# 绘制车位
for i in range(车位数量):
    组数 = i // 每组车位数
    行数 = 组数 // 每行组数
    组内编号 = i % 每组车位数
    行内组编号 = 组数 % 每行组数

    x = x_offset + 行内组编号 * (每组车位数 * 车位宽度 + 柱子宽度) + 组内编号 * 车位宽度
    y = y_offset + 行数 * (车位长度 + 车道宽度)

    车位实例 = 车位(2.4, 5.4, '水平', (x, y))


    # 判断车位是否与核心筒相交，若相交则不绘制该车位和相应的柱子
    if x + 车位宽度 <= 核心筒左上角[0] or x >= 核心筒右下角[0] or y + 车位宽度 <= 核心筒左上角[1] or y >= 核心筒右下角[1]:
        车位列表.append(车位实例)
        ax.add_patch(plt.Rectangle(车位实例.位置, 车位实例.长度, 车位实例.宽度, fill=False, edgecolor='black'))

        # 每组车位后绘制一个柱子
        if 组内编号 == 每组车位数 - 1 and 行内组编号 != 每行组数 - 1:
            柱位置x = x + 车位宽度
            柱位置y = y+ 车位长度/2
            柱子实例 = 柱(0.5,0.5,(柱位置x, 柱位置y))
            ax.add_patch(plt.Rectangle(柱子实例.位置, 柱子实例.长度, 柱子实例.宽度, fill=False, edgecolor='blue'))

# 绘制核心筒
核心筒实例 = 核心筒(10, 10, (核心筒位置x, 核心筒位置y))
ax.add_patch(plt.Rectangle(核心筒实例.位置, 核心筒实例.长度, 核心筒实例.宽度, fill=False, edgecolor='red'))

# 绘制车道
车道数量 = 内轮廓实例.宽度 // (车位长度 + 车道宽度)+1
for i in range(int(车道数量)):
    车道定位y = (车位长度 + 车道宽度) * i + 车位长度
    车道实例 = 车道(6, (内轮廓实例.长度 / 2, 车道定位y))

    ax.add_patch(plt.Rectangle((x_offset, 车道实例.中心定位点[1]), 车道长度, 车道实例.宽度, fill=False, edgecolor='gray'))

# 绘制车库
车库实例 = 车库(车道长度, (每行组数 * (车位长度 + 车道宽度) + 车道宽度),(x,y))
x=0
y=0
ax.add_patch(plt.Rectangle((0, 0), 车道长度 + (2 * (车位长度 + 车道宽度)), i*(车位长度+车道宽度)+2*车位长度+车道宽度, fill=False, edgecolor='purple'))

车库长度=车道长度+2*(车位长度+车道宽度)
车库宽度=i*(车位长度+车道实例.宽度)+2*车位长度+车道宽度

# 设置坐标轴范围
ax.set_xlim(0, 车库长度)
ax.set_ylim(0, 车库宽度)

# 计算车位数量
横向车位数量 = (车库长度-2 * 车位长度) // 车位宽度
纵向车位数量 = (车库宽度-2 * 车位长度) // 车位宽度
# 绘制上下两排车位
for i in range(int(横向车位数量)):
    x = i * 车位宽度 + 车位长度
    y1 = 0
    y2 = 车库宽度 - 车位长度
    车位1实例 = 车位(2.4, 5.4, '水平', (x, y1))
    ax.add_patch(plt.Rectangle((x, y1), 车位1实例.长度, 车位1实例.宽度, fill=False, edgecolor='black'))
    车位2实例 = 车位(2.4, 5.4, '水平', (x, y2))
    ax.add_patch(plt.Rectangle((x, y2), 车位2实例.长度, 车位2实例.宽度, fill=False, edgecolor='black'))

# 绘制左右两排车位
for k in range(int(纵向车位数量)):
    y = k * 车位宽度 + 车位长度
    x1 = 0
    x2 = 车库长度 - 车位长度
    车位3实例 = 车位(5.4, 2.4, '水平', (x1, y))
    车位4实例 = 车位(5.4, 2.4, '水平', (x2, y))
    ax.add_patch(plt.Rectangle((x1, y), 车位3实例.长度, 车位3实例.宽度, fill=False, edgecolor='black'))
    ax.add_patch(plt.Rectangle((x2, y), 车位4实例.长度, 车位4实例.宽度, fill=False, edgecolor='black'))

# 显示图形
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.show()