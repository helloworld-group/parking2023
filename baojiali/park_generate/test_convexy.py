from shapely.geometry import Polygon

# 给定矩形的左下角和右上角坐标
bottom_left = (5.4, 0)
top_right = (7.8, 5.4)

# 计算其他两个顶点
top_left = (bottom_left[0], top_right[1])
bottom_right = (top_right[0], bottom_left[1])

# 按顺时针或逆时针顺序排列四个顶点
# 这里按顺时针方向排列：左下角 -> 右下角 -> 右上角 -> 左上角
rectangle_coords = [bottom_left, bottom_right, top_right, top_left, bottom_left]  # 闭合多边形

# 使用 shapely 构建多边形
rectangle = Polygon(rectangle_coords)

# 输出多边形的边界坐标
print("矩形的边界坐标:", list(rectangle.exterior.coords))

# 检查多边形的有效性
print("多边形是否有效:", rectangle.is_valid)

# 检查多边形的面积
print("多边形的面积:", rectangle.area)

# 检查多边形的周长
print("多边形的周长:", rectangle.length)

# 如果你想可视化多边形，可以使用 matplotlib
import matplotlib.pyplot as plt

# 提取多边形的外部边界坐标
x, y = rectangle.exterior.xy

# 绘制多边形
plt.plot(x, y, color='blue', linewidth=2, solid_capstyle='round', zorder=2)
plt.fill(x, y, color='lightblue', alpha=0.5)
plt.scatter(*zip(*rectangle_coords), color='red')  # 标记顶点
plt.title("矩形多边形")
plt.xlabel("X 坐标")
plt.ylabel("Y 坐标")
plt.grid(True)
plt.show()