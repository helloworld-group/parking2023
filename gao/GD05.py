import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class depot:
    def __init__(self, length, width, orientation, position):
        self.length = length
        self.width = width
        self.orientation = orientation
        self.position = position

class obstacle:
    def __init__(self, length, width, position):
        self.length = length
        self.width = width
        self.position = position

class core(obstacle):
    pass
class column(obstacle):
    pass

class line:
    def __init__(self, width3, pt):
        self.width = width3
        self.point = pt

class outline:
    def __init__(self, length, width):
        self.length = length
        self.width = width
class plot(outline):
    pass

# 创建空的图形对象
fig, ax = plt.subplots()

# 创建类的实例
outline = outline(120, 60)
list= []
amount = 224
length1 = 5.4
width1= 2.4
length2 = 0.5
width2 = 0.5
length5 = 8.4*3
width5 = 8.4*3
width3 = 6
group = 3
length = outline.length - width1 * group

# 新的车位布局模式，两行车位之间有一个车道
# 每两行车位之间的间隔，考虑了车道的宽度
gap = width3 + length1

# 新的车位的Y轴起始位置
y_offset = gap

# 每组车位数量为3，每组车位后有一个柱子1
grouppl = outline.length // (group * width1 + width2)

# 单行车位的X轴起始位置
x_offset = length1 + width3

# 车位布局逻辑，确保车位不会出现在核心筒内并且不与核心筒产生交叉
for i in range(amount):
    组数 = i // group
    行数 = 组数 // grouppl
    组内编号 = i % group
    行内组编号 = 组数 % grouppl

    # 计算核心筒占用的位置范围
    核心筒位置x = (outline.length - length2) / 2
    核心筒位置y = (outline.width - width2) / 2
    核心筒左上角 = (核心筒位置x, 核心筒位置y)
    核心筒右下角 = (核心筒位置x + length2, 核心筒位置y + width2)

    x = x_offset + 行内组编号 * (group * width1 + width2) + 组内编号 * width1
    y = y_offset + 行数 * (length1 + gap)
    y1 = y + length1

    # 判断车位是否与核心筒相交
    if (
        x + width1 <= 核心筒左上角[0] or
        x >= 核心筒右下角[0] or
        y + length1 <= 核心筒左上角[1] or
        y >= 核心筒右下角[1] or
        y1 + length1 <= 核心筒左上角[1] or
        y1 >= 核心筒右下角[1]
    ):
        # 绘制车位矩形
        车位实例1 = depot(2.4, 5.4, '水平', (x, y))
        车位实例2 = depot(2.4, 5.4, '水平', (x, y1))
        ax.add_patch(plt.Rectangle((x, y), width1, length1, fill=False, edgecolor='black'))
        ax.add_patch(plt.Rectangle((x, y1), width1, length1, fill=False, edgecolor='black'))

        # 每组车位后绘制一个柱子
        if 组内编号 == group - 1 and 行内组编号 != grouppl - 1:
            柱位置x = x + width1
            柱位置y = y + length1 / 2
            柱子实例0 = column(0.5, 0.5, (柱位置x, 柱位置y))
            柱子实例 = column(0.5, 0.5, (柱位置x, 柱位置y + length1))
            ax.add_patch(plt.Rectangle(柱子实例0.位置, 柱子实例0.长度, 柱子实例0.宽度, fill=False, edgecolor='blue'))
            ax.add_patch(plt.Rectangle(柱子实例.位置, 柱子实例.长度, 柱子实例.宽度, fill=False, edgecolor='blue'))


# 绘制车道
车道数量 = outline.width // (length1 + width3)+1
for i in range(int(车道数量)):
    车道定位y = (length1*2 + width3) * i + length1
    车道实例 = outline(6, (outline.length / 2, 车道定位y))

    ax.add_patch(plt.Rectangle((x_offset, 车道实例.中心定位点[1]), length5, 车道实例.宽度, fill=False, edgecolor='gray'))

# 绘制车库
车库实例 = plot(length5, (grouppl * (length1 + width3) + width3),(x,y))
x=0
y=0
ax.add_patch(plt.Rectangle((0, 0), length5 + (2 * (length1 + width3)), 行数 * length1 * 2 + 车道数量*width3 + 4*length1, fill=False, edgecolor='purple'))

#建立车库长度和宽度
length6 = length5+2*(length1+width3)
width6 = 行数 * length1 * 2 + 车道数量 * width3 + 4 * length1

# 设置坐标轴范围
ax.set_xlim(0, length6)
ax.set_ylim(0, width6)

# 计算车位数量
Xamount = (length6-2 * length1) // width1
Yamount = (width6-2 * length1) // width1

# 修改后的绘制上下两排车位的部分
for i in range(amount):
    组数 = i // group
    行数 = 组数 // grouppl
    组内编号 = i % group
    行内组编号 = 组数 % grouppl

    x = length1 + 行内组编号 * (group * width1 + width2) + 组内编号 * width1
    y1 = 0
    y2 = width6 - length1

    车位1实例 = depot(2.4, 5.4, '水平', (x, y1))
    车位2实例 = depot(2.4, 5.4, '水平', (x, y2))
    ax.add_patch(plt.Rectangle((x, y1), width1, length1, fill=False, edgecolor='black'))
    ax.add_patch(plt.Rectangle((x, y2), width1, length1, fill=False, edgecolor='black'))

    # 每组车位后绘制一个柱子
    if 组内编号 == group - 1 and 行内组编号 != grouppl - 1:
        柱位置x = x + width1
        柱位置y1 = y1 + length1 / 2
        柱位置y2 = y2 + length1 / 2
        柱子实例1 = column(0.5, 0.5, (柱位置x, 柱位置y1))
        柱子实例2 = column(0.5, 0.5, (柱位置x, 柱位置y2))
        ax.add_patch(plt.Rectangle(柱子实例1.位置, 柱子实例1.长度, 柱子实例1.宽度, fill=False, edgecolor='blue'))
        ax.add_patch(plt.Rectangle(柱子实例2.位置, 柱子实例2.长度, 柱子实例2.宽度, fill=False, edgecolor='blue'))


# 绘制左右两排车位
for k in range(int(Yamount)):
    组数1 = k // group
    行数1 = 组数1 // grouppl
    组内编号1 = k % group
    行内组编号1 = 组数1 % grouppl

    y = length1 + 行内组编号1 * (group * width1 + width2) + 组内编号1 * width1
    x1 = 0
    x2 = length6 - length1
    车位3实例 = depot(5.4, 2.4, '水平', (x1, y))
    车位4实例 = depot(5.4, 2.4, '水平', (x2, y))
    ax.add_patch(plt.Rectangle((x1, y), 车位3实例.长度, 车位3实例.宽度, fill=False, edgecolor='black'))
    ax.add_patch(plt.Rectangle((x2, y), 车位4实例.长度, 车位4实例.宽度, fill=False, edgecolor='black'))

    # 每组车位后绘制一个柱子
    if 组内编号1 == group - 1 and 行内组编号1 != grouppl - 1:
        柱位置x1 = x1 + length1/2
        柱位置x2 = x2 + length1/2
        柱位置y = y + width1
        柱子实例3 = column(0.5, 0.5, (柱位置x1, 柱位置y))
        柱子实例4 = column(0.5, 0.5, (柱位置x2, 柱位置y))
        ax.add_patch(plt.Rectangle(柱子实例3.位置, 柱子实例3.长度, 柱子实例3.宽度, fill=False, edgecolor='blue'))
        ax.add_patch(plt.Rectangle(柱子实例4.位置, 柱子实例4.长度, 柱子实例4.宽度, fill=False, edgecolor='blue'))

# 显示图形，略去不重要部分

plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.show()