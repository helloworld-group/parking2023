import matplotlib.pyplot as plt
import numpy as np


def plot_polygon(coordinates,fill_color='lightblue',line_color='black'):
    # 将多边形坐标转换为numpy数组
    # 将多边形坐标转换为numpy数组
    polygon = np.array(coordinates + [coordinates[0]])

    # 绘制多边形
    # plt.figure()
    plt.fill(polygon[:, 0], polygon[:, 1], color=fill_color, edgecolor='black')
    plt.plot(polygon[:, 0], polygon[:, 1], color=line_color)

    # 设置图形属性
    plt.title('Closed Polygon Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    
    # 显示图形
    plt.show()


if __name__ == "__main__":
    # 替换为实际的二维点坐标元组列表
    point_coordinates = [(0, 0), (5, 0), (5, 5), (2,5),(2,2),(0, 2)]

    # 绘制多边形
    plot_polygon(point_coordinates)
    aaa=1
