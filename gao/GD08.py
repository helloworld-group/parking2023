from shapely.geometry import Point, Polygon, JOIN_STYLE, CAP_STYLE
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from typing import List
from shapely.affinity import translate
from math import isclose

def show_polygon(polygon):
    p = gpd.GeoSeries(polygon)
    p.plot()
    plt.show()


def show_matrix(matrix: List[List]):
    plt.matshow(matrix)
    plt.gca().invert_yaxis()
    plt.show()


def show_points(points):
    x1, y1 = zip(*points)
    plt.scatter(x1, y1, color='blue', label='Points Set 1')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('Scatter Plot of Points Sets')
    plt.legend()
    plt.show()


def show_layouts(layouts: []):
    fig, ax = plt.subplots()
    for rectangle in layouts:
        x = [point[0] for point in rectangle]+[rectangle[0][0]]
        y = [point[1] for point in rectangle]+[rectangle[0][1]]
        ax.plot(x, y, marker='o', markersize=0, linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    # 保持xy比例一致
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('Length/m')
    plt.ylabel('Width/m')
    plt.title('Parking Site')
    plt.grid(True)
    plt.show()


def range_iterator(start, end, step):
    current = start
    while (start < end and current < end) or (start > end and current > end):
        yield current
        current += step if start < end else -step


def judge_concavity(point1, point2, point3):
    line1 = point1-point2
    line2 = point3-point2
    if np.cross(line1, line2) > 0:
        return True
    return False


# 输入第一行为 n，表示有 n 个多边形
# 接下来为 a1,a2,a3,...,an，表示每个多边形的类型，正数代表加入，负数代表挖去
# 接下来 n 行，每行 ai ，代表多边形的坐标

nun_polygons = 0
input_polygons_type = []
input_points_list = []
input_polygons_list = []
polygon = Polygon()

eps = 1e-6

with open('GD08-input.txt', 'r') as f:
    num_polygons = int(f.readline())
    for num in f.readline().split():
        input_polygons_type.append(int(num) >= 0)
    for i in range(num_polygons):
        input_points_list.append([])
        for coordinates in f.readline().split():
            input_points_list[i].append(
                (float(coordinates.split(',')[0]), float(coordinates.split(',')[1])))
        input_polygons_list.append(Polygon(input_points_list[i]))
        if input_polygons_type[i] == True:
            polygon = polygon.union(input_polygons_list[i])
        else:
            polygon = polygon.difference(input_polygons_list[i])
print(num_polygons)
# polygon = polygon.buffer(-4.5, join_style=JOIN_STYLE.mitre,
#                          cap_style=CAP_STYLE.square)
show_polygon(polygon)

def translate_to_first_quadrant(polygon):
    # 获取多边形的当前位置（边界框的最小点）
    min_x, min_y, _, _ = polygon.bounds
    # 计算需要平移的距离
    translation_x = -min_x
    translation_y = -min_y
    # 平移多边形
    translated_polygon = translate(
        polygon, xoff=translation_x, yoff=translation_y)
    return translated_polygon


def polygon_discrete(polygon: Polygon, step: float):
    min_x, min_y, max_x, max_y = map(
        int, tuple(x/step for x in polygon.bounds))
    points_matrix = [[0 for i in range(0, max_x)]
                     for j in range(0, max_y)]
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            point = Point(x*step, y*step)
            if polygon.contains(point):
                points_matrix[y][x] = 1
    # show_polygon(polygon)
    show_matrix(points_matrix)
    return points_matrix


def points_separate(points: List[List]):
    def is_all_zero(matrix) -> bool:
        for row in matrix:
            for element in row:
                if element != 0:
                    return False
        return True

    def max_rectangle(matrix, start_row, start_col):
        rows = len(matrix)
        cols = len(matrix[start_row])
        # 从给定起始点开始，横向扩展
        width = 0
        # 计算当前横向扩展的宽度
        for j in range(start_col, cols):
            if matrix[start_row][j] == 1:
                width += 1
            else:
                break
        # 逐行向上检查该宽度内的矩形面积
        height = 1
        for i in range(start_row+1, rows):
            cur_width = 0
            for j in range(start_col, start_col+width):
                if matrix[i][j] == 1:
                    cur_width += 1
                else:
                    break
            if cur_width == width:
                height += 1
            else:
                break
        return width, height
    polygons_separated = []
    while is_all_zero(points) == False:
        for y in range(len(points)):
            for x in range(len(points[y])):
                if points[y][x] == 1:
                    width, height = max_rectangle(points, y, x)
                    # if width == 1 or height == 1:
                    #     continue
                    polygons_separated.append(
                        [(x, y), (x+width-1, y), (x+width-1, y+height-1), (x, y+height-1)])
                    print(width, height)
                    for i in range(y, y+height):
                        for j in range(x, x+width):
                            points[i][j] = 0
    return polygons_separated


polygon = translate_to_first_quadrant(polygon)
buffer_polygon = polygon.buffer(-5, join_style=JOIN_STYLE.mitre,)
points_separated = polygon_discrete(buffer_polygon, 1)
points_bounds = points_separate(points_separated)


# 扫描线
def scan_line(polygon: Polygon, step: float):
    # 将多边形平移到第一象限
    polygon = translate_to_first_quadrant(polygon)
    # 将多边形离散化
    points_matrix = polygon_discrete(polygon, step)
    # 将多边形分割成若干个矩形
    polygons_separated = points_separate(points_matrix)
    # 将矩形转换为多边形
    polygons = []
    for points in polygons_separated:
        polygons.append(Polygon(points))
    # 将多边形进行合并
    polygons_merged = unary_union(polygons)
    # 将多边形进行缓冲
    polygons_merged = polygons_merged.buffer(eps, join_style=JOIN_STYLE.mitre,
                                             cap_style=CAP_STYLE.square)
    # 将多边形进行平移
    polygons_merged = translate_to_first_quadrant(polygons_merged)
    # 将多边形进行缓冲
    polygons_merged = polygons_merged.buffer(-eps, join_style=JOIN_STYLE.mitre,
                                             cap_style=CAP_STYLE.square)
    # 显示多边形
    show_polygon(polygons_merged)
    # 显示多边形的顶点
    for point in polygons_merged.exterior.coords:
        print(point[0], point[1])
    # 显示多边形的边
    for line in polygons_merged.exterior.coords:
        print(line[0], line[1])
    # 显示多边形的面积
    print(polygons_merged.area)
    # 显示多边形的周长
    print(polygons_merged.length)


def inner_layout(point_bounds: [tuple], layout_type: int, car_bounds=[2.5, 5.5], step=6):
    car_layouts = []
    point_bounds = np.array(point_bounds)
    min_x, min_y, max_x, max_y = np.min(
        point_bounds[:, 0]), np.min(point_bounds[:, 1]), np.max(point_bounds[:, 0]), np.max(point_bounds[:, 1])
    car_x = car_bounds[0]
    car_y = car_bounds[1]
    min_x, min_y, max_x, max_y = min_x+step / \
        2, min_y+step/2, max_x-step/2, max_y-step/2
    print(min_x, min_y, max_x, max_y)

    count_num = 0
    i = min_x
    while i < max_x-car_y:
        count_num += 1
        for j in np.arange(min_y, max_y, car_x):
            car_layouts.append(
                [(i, j), (i+car_y, j), (i+car_y, j+car_x), (i, j+car_x)])
        if count_num == 2:
            i += step
            count_num = 0
        i += car_y
    return car_layouts


car_layouts = []
for x in points_bounds:
    car_layouts.extend(inner_layout(x, 0))
# show_layouts(car_layouts)


def outer_layout(polygon, car_bounds=[2.5, 5.5]):
    cur_polygon = Polygon()
    car_layouts = []
    # display(polygon)
    ex_points = polygon.exterior.coords
    in_points_list = [x.coords for x in polygon.interiors]
    # print(*ex_points)
    # print(*in_points_list[0])

    ex_points = ex_points[:-1]
    for i in range(len(ex_points)):
        cur_point = np.array(ex_points[i])
        next_point = np.array(ex_points[(i+1) % len(ex_points)])
        next_next_point = np.array(ex_points[(i+2) % len(ex_points)])
        pre_point = np.array(ex_points[(i-1) % len(ex_points)])
        line1 = next_point-cur_point
        line2 = pre_point-cur_point

        concavity_cur = judge_concavity(pre_point, cur_point, next_point)
        concavity_next = judge_concavity(
            cur_point, next_point, next_next_point)
        if not concavity_cur and not concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(cur_point[1], next_point[1]+car_bounds[1]*directiony, car_bounds[0]):
                    car_layouts.append([(cur_point[0], j), (cur_point[0]+car_bounds[1]*directionx, j),
                                        (cur_point[0]+car_bounds[1]*directionx, j+car_bounds[0]*directiony), (cur_point[0], j+car_bounds[0]*directiony)])
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] < 0 else -1
                for j in range_iterator(cur_point[0], next_point[0]+car_bounds[1]*directionx, car_bounds[0]):
                    car_layouts.append([(j, cur_point[1]), (j+car_bounds[0]*directionx, cur_point[1]),
                                        (j+car_bounds[0]*directionx, cur_point[1]+car_bounds[1]*directiony), (j, cur_point[1]+car_bounds[1]*directiony)])
        if concavity_cur and not concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(cur_point[1]+car_bounds[1]*directiony, next_point[1]+car_bounds[1]*directiony, car_bounds[0]):
                    car_layouts.append([(cur_point[0], j), (cur_point[0]+car_bounds[1]*directionx, j),
                                        (cur_point[0]+car_bounds[1]*directionx, j+car_bounds[0]*directiony), (cur_point[0], j+car_bounds[0]*directiony)])
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] > 0 else -1
                for j in range_iterator(cur_point[0]+car_bounds[1]*directionx, next_point[0]+car_bounds[1]*directionx, car_bounds[0]):
                    car_layouts.append([(j, cur_point[1]), (j+car_bounds[0]*directionx, cur_point[1]),
                                        (j+car_bounds[0]*directionx, cur_point[1]+car_bounds[1]*directiony), (j, cur_point[1]+car_bounds[1]*directiony)])
        if concavity_cur and concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(cur_point[1]+car_bounds[1]*directiony, next_point[1]-car_bounds[1]*directiony, car_bounds[0]):
                    car_layouts.append([(cur_point[0], j), (cur_point[0]+car_bounds[1]*directionx, j),
                                        (cur_point[0]+car_bounds[1]*directionx, j+car_bounds[0]*directiony), (cur_point[0], j+car_bounds[0]*directiony)])
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] > 0 else -1
                for j in range_iterator(cur_point[0]+car_bounds[1]*directionx, next_point[0]-car_bounds[1]*directionx, car_bounds[0]):
                    car_layouts.append([(j, cur_point[1]), (j+car_bounds[0]*directionx, cur_point[1]),
                                        (j+car_bounds[0]*directionx, cur_point[1]+car_bounds[1]*directiony), (j, cur_point[1]+car_bounds[1]*directiony)])
        if not concavity_cur and concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] < 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(cur_point[1], next_point[1]-car_bounds[1]*directiony, car_bounds[0]):
                    car_layouts.append([(cur_point[0], j), (cur_point[0]+car_bounds[1]*directionx, j),
                                        (cur_point[0]+car_bounds[1]*directionx, j+car_bounds[0]*directiony), (cur_point[0], j+car_bounds[0]*directiony)])
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] < 0 else -1
                for j in range_iterator(cur_point[0], next_point[0]-car_bounds[1]*directionx, car_bounds[0]):
                    car_layouts.append([(j, cur_point[1]), (j+car_bounds[0]*directionx, cur_point[1]),
                                        (j+car_bounds[0]*directionx, cur_point[1]+car_bounds[1]*directiony), (j, cur_point[1]+car_bounds[1]*directiony)])

    for car_layout in car_layouts:
        cur_polygon = cur_polygon.union(Polygon(car_layout))
    show_polygon(cur_polygon)

    for in_points in in_points_list:
        min_x = min(in_points[:-1], key=lambda point: point[0])[0]
        max_x = max(in_points[:-1], key=lambda point: point[0])[0]
        min_y = min(in_points[:-1], key=lambda point: point[1])[1]
        max_y = max(in_points[:-1], key=lambda point: point[1])[1]
        for x in range_iterator(min_x-car_bounds[1], max_x+car_bounds[1]-car_bounds[0], car_bounds[0]):
            polygon1 = [(x, min_y), (x+car_bounds[0], min_y),
                        (x+car_bounds[0], min_y-car_bounds[1]), (x, min_y-car_bounds[1])]
            ppolygon1 = Polygon(polygon1).buffer(5)
            if ppolygon1.intersects(cur_polygon) == False:
                car_layouts.append(polygon1)

            polygon2 = [(x, max_y), (x+car_bounds[0], max_y),
                        (x+car_bounds[0], max_y+car_bounds[1]), (x, max_y+car_bounds[1])]
            ppolygon2 = Polygon(polygon2).buffer(5)
            if ppolygon2.intersects(cur_polygon) == False:
                car_layouts.append(polygon2)

        for y in range_iterator(min_y, max_y-car_bounds[0], car_bounds[0]):
            polygon1 = [(min_x, y), (min_x-car_bounds[1], y),
                        (min_x-car_bounds[1], y+car_bounds[0]), (min_x, y+car_bounds[0])]
            polygon2 = [(max_x, y), (max_x+car_bounds[1], y),
                        (max_x+car_bounds[1], y+car_bounds[0]), (max_x, y+car_bounds[0])]
            ppolygon1 = Polygon(polygon1).buffer(5)
            if ppolygon1.intersects(cur_polygon) == False:
                car_layouts.append(polygon1)
            ppolygon2 = Polygon(polygon2).buffer(5)
            if ppolygon2.intersects(cur_polygon) == False:
                car_layouts.append(polygon2)

    return car_layouts

outer_car_layouts = outer_layout(polygon)
show_layouts(outer_car_layouts)
car_layouts.extend(outer_car_layouts)
show_layouts(car_layouts)