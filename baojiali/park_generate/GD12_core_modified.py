import numpy as np

# from PIL._imaging import display
from matplotlib import patches
from shapely.geometry import Point, Polygon, LineString
from shapely import buffer
import matplotlib.pyplot as plt
import geopandas as gpd
from typing import List
from math import isclose
import random


class CFG:
    rand_times = 2  # 随机次数上线
    min_size = 0.2  # 拓展精度
    min_area_rate = 0.01
    eps = 1e-6
    car_width = 2.4  # 车宽度
    car_length = 5.4  # 车长度
    pillar_width = 0.4  # 柱子宽度
    pillar_length = 0.8  # 柱子长度
    road_width = 5.5  # 道路宽度
    car_group_limit = 5  # 车道组数
    vertical_group_size=2 # the vertical maximum vehicles inside the group
    horizontal_group_size=4 # the horizontal maximum vehicles inside the group
    min_division_width = 17 # 最小分割宽度
    min_division_height = 17  # 最小分割高度
    division_repeat_time = 30 # 最小分割重复次数
    


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
    plt.scatter(x1, y1, color="blue", label="Points Set 1")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Scatter Plot of Points Sets")
    plt.legend()
    plt.show()


def show_layouts(layouts: [tuple], axis_range):
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    ax.set_xlim(axis_range[0], axis_range[2])
    ax.set_ylim(axis_range[1], axis_range[3])
    for i, bounds in enumerate(layouts):
        min_x, min_y, max_x, max_y = bounds
        rectangle = patches.Rectangle(
            (min_x, min_y),
            max_x - min_x,
            max_y - min_y,
            linewidth=0.5,
            edgecolor="black",
            facecolor="yellow",
        )
        rx, ry = rectangle.get_xy()
        cx = rx + rectangle.get_width() / 2.0
        cy = ry + rectangle.get_height() / 2.0
        area = abs((max_x - min_x) * (max_y - min_y))
        ax.annotate(
            f"No.{i+1}\narea:{area:.2f}",
            (cx, cy),
            color="black",
            fontsize=5,
            ha="center",
            va="center",
        )
        ax.add_patch(rectangle)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    # 保持xy比例一致
    ax.set_aspect("equal", adjustable="box")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Rectangles Plot")
    plt.grid(True)
    plt.show()


def show_car_and_pillar(car, pillar, obstacles, axis_range):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_xlim(axis_range[0], axis_range[2])
    ax.set_ylim(axis_range[1], axis_range[3])
    for bounds in car:
        min_x, min_y, max_x, max_y = bounds
        ax.plot(
            [min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y],
            color="black",
            linewidth=0.5,
        )
    for bounds in pillar:
        min_x, min_y, max_x, max_y = bounds
        ax.plot(
            [min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y],
            color="red",
            linewidth=0.5,
        )
    for obstacle in obstacles:
        min_x, min_y, max_x, max_y = obstacle.bounds
        ax.plot(
            [min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y],
            color="blue",
            linewidth=0.5,
        )

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    # 保持xy比例一致
    ax.set_aspect("equal", adjustable="box")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Rectangles Plot")
    plt.grid(True)
    plt.show()
    aaa = 1


def range_iterator(start, end, step):
    current = start
    while (start < end and current < end) or (start > end and current > end):
        yield current
        current += step if start < end else -step


def judge_concavity(point1, point2, point3):
    line1 = point1 - point2
    line2 = point3 - point2
    if np.cross(line1, line2) > 0:
        return True
    return False


# %%
def read_input(path: str) -> Polygon:
    nun_polygons = 0
    input_polygons_type = []
    input_points_list = []
    input_polygons_list = []
    obstacles = []
    polygon = Polygon()
    with open(path, "r") as f:
        num_polygons = int(f.readline())
        for num in f.readline().split():
            input_polygons_type.append(int(num) >= 0)
        for i in range(num_polygons):
            input_points_list.append([])
            for coordinates in f.readline().split():
                input_points_list[i].append(
                    (float(coordinates.split(",")[0]), float(coordinates.split(",")[1]))
                )
            input_polygons_list.append(Polygon(input_points_list[i]))
            if input_polygons_type[i] == True:

                polygon = polygon.union(input_polygons_list[i])
            else:
                obstacles.append(input_polygons_list[i])
                # polygon = polygon.difference(input_polygons_list[i])
    return polygon, obstacles


# %%
def find_first_intersection(point: Point, polygon: Polygon, type):
    min_x, min_y, max_x, max_y = polygon.bounds
    if type == "x+":
        line = LineString([(point.x, point.y), (max_x + 1, point.y)])
    elif type == "x-":
        line = LineString([(point.x, point.y), (min_x - 1, point.y)])
    elif type == "y+":
        line = LineString([(point.x, point.y), (point.x, max_y + 1)])
    elif type == "y-":
        line = LineString([(point.x, point.y), (point.x, min_y - 1)])
    intersection = line.intersection(polygon)
    if intersection.geom_type == "LineString":
        return intersection.coords[-1]
    elif intersection.geom_type == "MultiLineString":
        return intersection.geoms[0].coords[-1]
    elif intersection.geom_type == "MultiPoint":
        return intersection[0]
    elif intersection.geom_type == "Point":
        return intersection
    elif intersection.geom_type == "GeometryCollection":
        # for a in intersection:
        #     display(a)
        return intersection.geoms[0].coords[-1]
    else:
        display(intersection)
        display(intersection.geom_type)
        return None


def expand_line(line: LineString, polygon: Polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    start_x = line.coords[0][0]
    end_x = line.coords[-1][0]
    origin_y = line.coords[0][1]
    start_y = min_y
    end_y = max_y
    for x in np.arange(start_x + CFG.eps, end_x - CFG.eps, CFG.min_size):
        cur_point = Point(x, origin_y)
        point1 = find_first_intersection(cur_point, polygon, "y+")
        point2 = find_first_intersection(cur_point, polygon, "y-")
        start_y = max(start_y, point2[1])
        end_y = min(end_y, point1[1])
    return (start_y, end_y)


def random_cut_polygon(polygon: Polygon):
    ret_list = []
    min_x, min_y, max_x, max_y = polygon.bounds
    origin_area = polygon.area
    while polygon.area > origin_area * CFG.min_area_rate:
        rand_x = random.uniform(min_x, max_x)
        rand_y = random.uniform(min_y, max_y)
        cur_point = Point(rand_x, rand_y)
        if polygon.contains(cur_point):
            point1 = find_first_intersection(cur_point, polygon, "x-")
            point2 = find_first_intersection(cur_point, polygon, "x+")
            line_x = LineString([point1, point2])
            start_x, end_x = point1[0], point2[0]
            start_y, end_y = expand_line(line_x, polygon)
            cur_polygon = Polygon(
                [(start_x, start_y), (end_x, start_y), (end_x, end_y), (start_x, end_y)]
            )
            polygon = polygon.difference(cur_polygon)
            ret_list.append((start_x, start_y, end_x, end_y))
    return ret_list


# maximum cut
def maximum_cut_polygon(polygon: Polygon):
    # repeat_times = 50
    ret_list = []
    min_x, min_y, max_x, max_y = polygon.bounds
    origin_area = polygon.area
    while polygon.area > origin_area * CFG.min_area_rate:
        cur_times = 0
        max_polygon_area = 0
        max_polygon = None
        max_start_x, max_start_y, max_end_x, max_end_y = 0, 0, 0, 0
        while True:
            if cur_times > CFG.division_repeat_time:
                break
            rand_x = random.uniform(min_x, max_x)
            rand_y = random.uniform(min_y, max_y)
            cur_point = Point(rand_x, rand_y)
            if polygon.contains(cur_point):
                cur_times += 1
                point1 = find_first_intersection(cur_point, polygon, "x-")
                point2 = find_first_intersection(cur_point, polygon, "x+")
                line_x = LineString([point1, point2])
                start_x, end_x = point1[0], point2[0]
                start_y, end_y = expand_line(line_x, polygon)
                # if the sampled rectangle does not fulfill the division width, height and surface requirement, skip
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                if width < CFG.min_division_width or height < CFG.min_division_height:
                    if width * height < 100:
                        continue
                cur_area = abs((start_x - end_x) * (start_y - end_y))
                if cur_area > max_polygon_area:
                    max_polygon = Polygon(
                        [
                            (start_x, start_y),
                            (end_x, start_y),
                            (end_x, end_y),
                            (start_x, end_y),
                        ]
                    )
                    max_start_x, max_end_x, max_start_y, max_end_y = (
                        start_x,
                        end_x,
                        start_y,
                        end_y,
                    )
                    max_polygon_area = cur_area
        if not max_polygon:
            break
        polygon = polygon.difference(max_polygon)
        print(polygon.area)
        ret_list.append((max_start_x, max_start_y, max_end_x, max_end_y))
    return ret_list
    pass


def vertical_parking_generate():
    pass

def inner_layout(polygon_bounds: tuple, layout_type: int):
    car_bounds_list = []
    pillar_bounds_list = []
    min_x, min_y, max_x, max_y = polygon_bounds
    car_width = CFG.car_width
    car_length = CFG.car_length
    # get the range of current rectangle
    min_x, min_y, max_x, max_y = (
        min_x + CFG.road_width / 2,
        min_y + CFG.road_width / 2,
        max_x - CFG.road_width / 2,
        max_y - CFG.road_width / 2,
    )
    
    if layout_type == 1:
        horizontal_pos = min_x
        horizontal_idx=0
        horizontal_idx_max=int((max_x-min_x)/CFG.car_width)
        vertical_idx_max=int((max_y-min_y)/CFG.car_length)

        # horizontally generate the parking slots until the end
        while horizontal_idx<horizontal_idx_max:
            # stop if the current position hits the horizontal limit
            if horizontal_pos>max_x - car_width:
                break        
            vertical_idx = 0
            vertical_pos = min_y
            
            # if we hit horizontally the limit of one group, ex, the fourth, we move with the width of pillar
            if horizontal_idx%CFG.horizontal_group_size==0 :
                # pillar_bounds_list.append((horizontal_pos,vertical_pos,horizontal_pos+CFG.pillar_width,vertical_pos+CFG.car_length))
                horizontal_pos+=CFG.pillar_width
            # vertically generate the parking slots until the end
            while vertical_idx<vertical_idx_max:

                # stop if the current position hits the vertical limit
                if vertical_pos > max_y - car_length:
                    break
                car_bounds_list.append([horizontal_pos, vertical_pos, horizontal_pos + car_width, vertical_pos + car_length])
                
                # when we start a new small group horizontally, we add the pillars 
                if horizontal_idx%CFG.horizontal_group_size==0:
                    # add a pillar at the bottom
                    x1=horizontal_pos-CFG.pillar_width/2
                    y1=vertical_pos-CFG.pillar_width/2
                    x2=horizontal_pos+CFG.pillar_width/2
                    y2=vertical_pos+CFG.pillar_width/2
                    
                    # if horizontal_idx!=0:
                    pillar_bounds_list.append((x1,y1,x2,y2))
                    pillar_bounds_list.append((x1,y1+CFG.car_length,x2,y2+CFG.car_length))
                    # add a pillar at the top
                    
                if horizontal_idx%CFG.horizontal_group_size==(CFG.horizontal_group_size-1):
                    # add a pillar at the bottom
                    x1=horizontal_pos-CFG.pillar_width/2+CFG.car_width
                    y1=vertical_pos-CFG.pillar_width/2
                    x2=horizontal_pos+CFG.pillar_width/2+CFG.car_width
                    y2=vertical_pos+CFG.pillar_width/2
                    
                    # if horizontal_idx!=0:
                    pillar_bounds_list.append((x1,y1,x2,y2))
                    pillar_bounds_list.append((x1,y1+CFG.car_length,x2,y2+CFG.car_length))
                    
                # if we vertically hit the limit of the big group, ex, the second row, we move across the road
                if vertical_idx%CFG.vertical_group_size==(CFG.vertical_group_size-1) :
                    vertical_pos+=CFG.road_width
                
                vertical_pos+=CFG.car_length
                vertical_idx+=1
                

            
            # if we horizontally hit the limit of group, ex, the 20th column, we move across the road
            if horizontal_idx%(CFG.horizontal_group_size*CFG.car_group_limit)==(CFG.horizontal_group_size*CFG.car_group_limit-1) :
                horizontal_pos+=CFG.road_width
                
            horizontal_pos+=CFG.car_width
            horizontal_idx+=1
                
                # if i%CFG.horizontal_group_size==0 and j%CFG.vertical_group_size==0:
                    
                
            
            
            # # vertically generate the parking slots until the end
            # while j < max_y - car_length:
            #     count_num_j += 1
            #     if count_num_i % CFG.group_size_limit == 1 and count_num_j % 2 == 1:
            #         if count_num_j == 1 and count_num_i == 1:
            #             i += CFG.pillar_width
            #         pillar_bounds_list.append(
            #             (i - CFG.pillar_width, j, i, j + CFG.pillar_length)
            #         )
            #         if j + car_length < max_y:
            #             pillar_bounds_list.append(
            #                 (
            #                     i - CFG.pillar_width,
            #                     j + car_length - CFG.pillar_length / 2,
            #                     i,
            #                     j + car_length + CFG.pillar_length / 2,
            #                 )
            #             )
            #         if j + car_length * 2 < max_y:
            #             pillar_bounds_list.append(
            #                 (
            #                     i - CFG.pillar_width,
            #                     j + car_length * 2 - CFG.pillar_length,
            #                     i,
            #                     j + car_length * 2,
            #                 )
            #             )
            #     car_bounds_list.append([i, j, i + car_width, j + car_length])
            #     if (
            #         count_num_i % 4 == 0 or i + car_width * 2 > max_x
            #     ) and count_num_j % 2 == 1:
            #         i += CFG.pillar_width
            #         pillar_bounds_list.append(
            #             (
            #                 i + car_width - CFG.pillar_width,
            #                 j,
            #                 i + car_width,
            #                 j + CFG.pillar_length,
            #             )
            #         )
            #         if j + car_length < max_y:
            #             pillar_bounds_list.append(
            #                 (
            #                     i + car_width - CFG.pillar_width,
            #                     j + car_length - CFG.pillar_length / 2,
            #                     i + car_width,
            #                     j + car_length + CFG.pillar_length / 2,
            #                 )
            #             )
            #         if j + car_length * 2 < max_y:
            #             pillar_bounds_list.append(
            #                 (
            #                     i + car_width - CFG.pillar_width,
            #                     j + car_length * 2 - CFG.pillar_length,
            #                     i + car_width,
            #                     j + car_length * 2,
            #                 )
            #             )
            #         i -= CFG.pillar_width
            #     if count_num_j % 2 == 0:
            #         j += CFG.road_width
            #     j += car_length
            # if count_num_i % 4 == 0:
            #     i += CFG.pillar_width
            # if count_num_i % (4 * CFG.car_group_limit) == 0:
            #     i += CFG.road_width
            # i += car_width
    else:
        count_num_i = 0
        i = min_x
        while i < max_x - car_length:
            count_num_i += 1
            count_num_j = 0
            j = min_y
            while j < max_y - car_width:
                count_num_j += 1
                if count_num_i % 4 == 1 and count_num_j % 2 == 1:
                    if count_num_j == 1 and count_num_i == 1:
                        i += CFG.pillar_length
                    pillar_bounds_list.append(
                        (i - CFG.pillar_length, j, i, j + CFG.pillar_width)
                    )
                    if j + car_width < max_y:
                        pillar_bounds_list.append(
                            (
                                i - CFG.pillar_length,
                                j + car_width - CFG.pillar_width / 2,
                                i,
                                j + car_width + CFG.pillar_width / 2,
                            )
                        )
                    if j + car_width * 2 < max_y:
                        pillar_bounds_list.append(
                            (
                                i - CFG.pillar_width,
                                j + car_width * 2 - CFG.pillar_width,
                                i,
                                j + car_width * 2,
                            )
                        )
                car_bounds_list.append([i, j, i + car_length, j + car_width])
                if (
                    count_num_i % 4 == 0 or i + car_length * 2 > max_x
                ) and count_num_j % 2 == 1:
                    i += CFG.pillar_length
                    pillar_bounds_list.append(
                        (
                            i + car_length - CFG.pillar_length,
                            j,
                            i + car_length,
                            j + CFG.pillar_width,
                        )
                    )
                    if j + car_width < max_y:
                        pillar_bounds_list.append(
                            (
                                i + car_length - CFG.pillar_length,
                                j + car_width - CFG.pillar_width / 2,
                                i + car_length,
                                j + car_width + CFG.pillar_width / 2,
                            )
                        )
                    if j + car_width * 2 < max_y:
                        pillar_bounds_list.append(
                            (
                                i + car_length - CFG.pillar_length,
                                j + car_width * 2 - CFG.pillar_width,
                                i + car_length,
                                j + car_width * 2,
                            )
                        )
                    i -= CFG.pillar_length
                if count_num_j % 2 == 0:
                    j += CFG.road_width
                j += car_width
            if count_num_i % 4 == 0:
                i += CFG.pillar_length
            if count_num_i % (4 * CFG.car_group_limit) == 0:
                i += CFG.road_width
            i += car_length

    return car_bounds_list, pillar_bounds_list




# def inner_layout(polygon_bounds: tuple, layout_type: int):
#     car_bounds_list = []
#     pillar_bounds_list = []
#     min_x, min_y, max_x, max_y = polygon_bounds
#     car_width = CFG.car_width
#     car_length = CFG.car_length
#     # get the range of current rectangle
#     min_x, min_y, max_x, max_y = (
#         min_x + CFG.road_width / 2,
#         min_y + CFG.road_width / 2,
#         max_x - CFG.road_width / 2,
#         max_y - CFG.road_width / 2,
#     )
#     if layout_type == 1:
#         count_num_i = 0
#         i = min_x

#         # horizontally generate the parking slots until the end
#         while i < max_x - car_width:
#             count_num_i += 1
#             count_num_j = 0
#             j = min_y
#             # vertically generate the parking slots until the end
#             while j < max_y - car_length:
#                 count_num_j += 1
#                 if count_num_i % CFG.group_size_limit == 1 and count_num_j % 2 == 1:
#                     if count_num_j == 1 and count_num_i == 1:
#                         i += CFG.pillar_width
#                     pillar_bounds_list.append(
#                         (i - CFG.pillar_width, j, i, j + CFG.pillar_length)
#                     )
#                     if j + car_length < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i - CFG.pillar_width,
#                                 j + car_length - CFG.pillar_length / 2,
#                                 i,
#                                 j + car_length + CFG.pillar_length / 2,
#                             )
#                         )
#                     if j + car_length * 2 < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i - CFG.pillar_width,
#                                 j + car_length * 2 - CFG.pillar_length,
#                                 i,
#                                 j + car_length * 2,
#                             )
#                         )
#                 car_bounds_list.append([i, j, i + car_width, j + car_length])
#                 if (
#                     count_num_i % 4 == 0 or i + car_width * 2 > max_x
#                 ) and count_num_j % 2 == 1:
#                     i += CFG.pillar_width
#                     pillar_bounds_list.append(
#                         (
#                             i + car_width - CFG.pillar_width,
#                             j,
#                             i + car_width,
#                             j + CFG.pillar_length,
#                         )
#                     )
#                     if j + car_length < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i + car_width - CFG.pillar_width,
#                                 j + car_length - CFG.pillar_length / 2,
#                                 i + car_width,
#                                 j + car_length + CFG.pillar_length / 2,
#                             )
#                         )
#                     if j + car_length * 2 < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i + car_width - CFG.pillar_width,
#                                 j + car_length * 2 - CFG.pillar_length,
#                                 i + car_width,
#                                 j + car_length * 2,
#                             )
#                         )
#                     i -= CFG.pillar_width
#                 if count_num_j % 2 == 0:
#                     j += CFG.road_width
#                 j += car_length
#             if count_num_i % 4 == 0:
#                 i += CFG.pillar_width
#             if count_num_i % (4 * CFG.car_group_limit) == 0:
#                 i += CFG.road_width
#             i += car_width
#     else:
#         count_num_i = 0
#         i = min_x
#         while i < max_x - car_length:
#             count_num_i += 1
#             count_num_j = 0
#             j = min_y
#             while j < max_y - car_width:
#                 count_num_j += 1
#                 if count_num_i % 4 == 1 and count_num_j % 2 == 1:
#                     if count_num_j == 1 and count_num_i == 1:
#                         i += CFG.pillar_length
#                     pillar_bounds_list.append(
#                         (i - CFG.pillar_length, j, i, j + CFG.pillar_width)
#                     )
#                     if j + car_width < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i - CFG.pillar_length,
#                                 j + car_width - CFG.pillar_width / 2,
#                                 i,
#                                 j + car_width + CFG.pillar_width / 2,
#                             )
#                         )
#                     if j + car_width * 2 < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i - CFG.pillar_width,
#                                 j + car_width * 2 - CFG.pillar_width,
#                                 i,
#                                 j + car_width * 2,
#                             )
#                         )
#                 car_bounds_list.append([i, j, i + car_length, j + car_width])
#                 if (
#                     count_num_i % 4 == 0 or i + car_length * 2 > max_x
#                 ) and count_num_j % 2 == 1:
#                     i += CFG.pillar_length
#                     pillar_bounds_list.append(
#                         (
#                             i + car_length - CFG.pillar_length,
#                             j,
#                             i + car_length,
#                             j + CFG.pillar_width,
#                         )
#                     )
#                     if j + car_width < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i + car_length - CFG.pillar_length,
#                                 j + car_width - CFG.pillar_width / 2,
#                                 i + car_length,
#                                 j + car_width + CFG.pillar_width / 2,
#                             )
#                         )
#                     if j + car_width * 2 < max_y:
#                         pillar_bounds_list.append(
#                             (
#                                 i + car_length - CFG.pillar_length,
#                                 j + car_width * 2 - CFG.pillar_width,
#                                 i + car_length,
#                                 j + car_width * 2,
#                             )
#                         )
#                     i -= CFG.pillar_length
#                 if count_num_j % 2 == 0:
#                     j += CFG.road_width
#                 j += car_width
#             if count_num_i % 4 == 0:
#                 i += CFG.pillar_length
#             if count_num_i % (4 * CFG.car_group_limit) == 0:
#                 i += CFG.road_width
#             i += car_length

#     return car_bounds_list, pillar_bounds_list


def is_clockwise(polygon):
    # 计算多边形面积的两倍
    area = 0
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        area += (x2 - x1) * (y2 + y1)
    return area > 0  # 返回面积的符号，用来判断顺时针还是逆时针


def check_convexity(polygon):
    n = len(polygon)
    if n < 3:
        return "多边形至少需要三个点"

    convexity = []
    clockwise = is_clockwise(polygon)

    for i in range(n):
        p1 = polygon[(i - 1) % n]
        p2 = polygon[(i) % n]
        p3 = polygon[(i + 1) % n]

        # 向量
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])

        # 叉积
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]

        # 判断凹凸性
        if clockwise:
            if cross_product > 0:
                convexity.append(False)  # "凹"
            else:
                convexity.append(True)  # "凸"
        else:
            if cross_product < 0:
                convexity.append(False)  # "凹"
            else:
                convexity.append(True)  # "凸"

    return convexity


def outer_layout(polygon, obstacles: List[Polygon] = []):
    def judge_concavity(point1, point2, point3):
        line1 = point1 - point2
        line2 = point3 - point2
        if np.cross(line1, line2) > 0:
            return True
        return False

    car_bounds = [CFG.car_width, CFG.car_length]
    cur_polygon = Polygon()
    car_layouts = []
    ex_points = polygon.exterior.coords
    in_points_list = [x.coords for x in polygon.interiors]

    ex_points = ex_points[:-1]
    convexity = check_convexity(ex_points)

    # generate the parking slots along the bounds of the whole parking area
    for i in range(len(ex_points)):
        cur_point = np.array(ex_points[i])
        next_point = np.array(ex_points[(i + 1) % len(ex_points)])
        next_next_point = np.array(ex_points[(i + 2) % len(ex_points)])
        pre_point = np.array(ex_points[(i - 1) % len(ex_points)])
        line1 = next_point - cur_point
        line2 = pre_point - cur_point

        concavity_cur = convexity[i]
        concavity_next = convexity[(i + 1) % len(ex_points)]
        limit = car_bounds[1] + car_bounds[0]
        if not concavity_cur and not concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(
                    cur_point[1],
                    next_point[1] + car_bounds[0] * directiony,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        cur_point[0],
                        j,
                        cur_point[0] + car_bounds[1] * directionx,
                        j + car_bounds[0] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] < 0 else -1
                for j in range_iterator(
                    cur_point[0],
                    next_point[0] + car_bounds[0] * directionx,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        j,
                        cur_point[1],
                        j + car_bounds[0] * directionx,
                        cur_point[1] + car_bounds[1] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
        if concavity_cur and not concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(
                    cur_point[1] + car_bounds[1] * directiony,
                    next_point[1] + car_bounds[0] * directiony,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        cur_point[0],
                        j,
                        cur_point[0] + car_bounds[1] * directionx,
                        j + car_bounds[0] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] > 0 else -1
                for j in range_iterator(
                    cur_point[0] + car_bounds[1] * directionx,
                    next_point[0] + car_bounds[0] * directionx,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        j,
                        cur_point[1],
                        j + car_bounds[0] * directionx,
                        cur_point[1] + car_bounds[1] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
        if concavity_cur and concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] > 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(
                    cur_point[1] + car_bounds[1] * directiony,
                    next_point[1] - limit * directiony,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        cur_point[0],
                        j,
                        cur_point[0] + car_bounds[1] * directionx,
                        j + car_bounds[0] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] > 0 else -1
                for j in range_iterator(
                    cur_point[0] + car_bounds[1] * directionx,
                    next_point[0] - limit * directionx,
                    car_bounds[0],
                ):
                    min_x, min_y, max_x, max_y = (
                        j,
                        cur_point[1],
                        j + car_bounds[0] * directionx,
                        cur_point[1] + car_bounds[1] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
        if not concavity_cur and concavity_next:
            if isclose(cur_point[0], next_point[0]):
                directionx = 1 if line2[0] < 0 else -1
                directiony = 1 if line1[1] > 0 else -1
                for j in range_iterator(
                    cur_point[1], next_point[1] - limit * directiony, car_bounds[0]
                ):
                    min_x, min_y, max_x, max_y = (
                        cur_point[0],
                        j,
                        cur_point[0] + car_bounds[1] * directionx,
                        j + car_bounds[0] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))
            else:
                directionx = 1 if line1[0] > 0 else -1
                directiony = 1 if line2[1] < 0 else -1
                for j in range_iterator(
                    cur_point[0], next_point[0] - limit * directionx, car_bounds[0]
                ):
                    min_x, min_y, max_x, max_y = (
                        j,
                        cur_point[1],
                        j + car_bounds[0] * directionx,
                        cur_point[1] + car_bounds[1] * directiony,
                    )
                    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
                    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
                    car_layouts.append((min_x, min_y, max_x, max_y))

    # filter the car_layouts to exclude the parking slots which collides with obstacles

    car_layout_filterd = []
    for car_layout in car_layouts:
        # if the parking slots collide with the obstacles, skip
        min_x, min_y, max_x, max_y = car_layout
        intersect_with_obstacle = False
        for obstalce in obstacles:
            car_polygon = Polygon(
                [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
            )
            if car_polygon.intersects(obstalce):
                intersect_with_obstacle = True
                break
        if intersect_with_obstacle:
            continue
        car_layout_filterd.append(car_layout)

    car_layouts = car_layout_filterd

    for car_layout in car_layouts:
        # if the parking slots collide with the obstacles, skip

        min_x, min_y, max_x, max_y = car_layout
        cur_polygon = cur_polygon.union(
            Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
        )
    show_polygon(cur_polygon)

    aaaa = 1

    # generate the parking slots sourronding inner polygon, which are the obstacles
    for in_points in in_points_list:
        min_x = min(in_points[:-1], key=lambda point: point[0])[0]
        max_x = max(in_points[:-1], key=lambda point: point[0])[0]
        min_y = min(in_points[:-1], key=lambda point: point[1])[1]
        max_y = max(in_points[:-1], key=lambda point: point[1])[1]
        for x in range_iterator(
            min_x - car_bounds[1], max_x + car_bounds[1] - car_bounds[0], car_bounds[0]
        ):
            polygon1 = [
                (x, min_y),
                (x + car_bounds[0], min_y),
                (x + car_bounds[0], min_y - car_bounds[1]),
                (x, min_y - car_bounds[1]),
            ]
            polygon2 = [
                (x, max_y),
                (x + car_bounds[0], max_y),
                (x + car_bounds[0], max_y + car_bounds[1]),
                (x, max_y + car_bounds[1]),
            ]
            ppolygon1 = Polygon(polygon1).buffer(CFG.road_width)
            if ppolygon1.intersects(cur_polygon) == False:
                car_layouts.append((x, min_y - car_bounds[1], x + car_bounds[0], min_y))
            ppolygon2 = Polygon(polygon2).buffer(CFG.road_width)
            if ppolygon2.intersects(cur_polygon) == False:
                car_layouts.append((x, max_y, x + car_bounds[0], max_y + car_bounds[1]))

        for y in range_iterator(min_y, max_y - car_bounds[0], car_bounds[0]):
            polygon1 = [
                (min_x, y),
                (min_x - car_bounds[1], y),
                (min_x - car_bounds[1], y + car_bounds[0]),
                (min_x, y + car_bounds[0]),
            ]
            polygon2 = [
                (max_x, y),
                (max_x + car_bounds[1], y),
                (max_x + car_bounds[1], y + car_bounds[0]),
                (max_x, y + car_bounds[0]),
            ]
            ppolygon1 = Polygon(polygon1).buffer(CFG.road_width)
            if ppolygon1.intersects(cur_polygon) == False:
                car_layouts.append((min_x - car_bounds[1], y, min_x, y + car_bounds[0]))
            ppolygon2 = Polygon(polygon2).buffer(CFG.road_width)
            if ppolygon2.intersects(cur_polygon) == False:
                car_layouts.append((max_x, y, max_x + car_bounds[1], y + car_bounds[0]))
    return car_layouts


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
            if abs(p.x - point.x) < CFG.eps and abs(p.y - point.y) < CFG.eps:
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


def main():
    polygon_input, obstacles = read_input("GD12-input.txt")
    min_x, min_y, max_x, max_y = polygon_input.bounds
    show_polygon(polygon_input)
    polygon_input_buffer = buffer(
        polygon_input, -CFG.car_length - CFG.road_width / 2, join_style="mitre"
    )
    show_polygon(polygon_input_buffer)

    for obstalce in obstacles:
        # obstalce=buffer(obstalce,CFG.road_width / 2,)
        # extend the obstacle vertically with road_width/2
        extended_obs_bound = []

        min_x_obs, min_y_obs, max_x_obs, max_y_obs = obstalce.bounds
        extended_obs_bound.append((min_x_obs, min_y_obs - CFG.road_width / 2))
        extended_obs_bound.append((max_x_obs, min_y_obs - CFG.road_width / 2))
        extended_obs_bound.append((max_x_obs, max_y_obs + CFG.road_width / 2))
        extended_obs_bound.append((min_x_obs, max_y_obs + CFG.road_width / 2))
        extended_obstacle = Polygon(extended_obs_bound)
        polygon_input_buffer = polygon_input_buffer.difference(extended_obstacle)

    show_polygon(polygon_input_buffer)

    best_num = 0
    best_car_layouts = []
    best_pillar_layouts = []

    # 矩形切割
    # for i in range(CFG.rand_times):
    polygon_bounds_list = maximum_cut_polygon(polygon_input_buffer)
    show_layouts(polygon_bounds_list, (min_x, min_y, max_x, max_y))
    # display(polygon_bounds_list)
    graph = from_rectangle_to_graph(polygon_bounds_list)
    for edge in graph.edges:
        print(edge)

    # 内部排布
    inner_layouts = []
    pillar_layouts = []
    for polygon_bounds in polygon_bounds_list:
        car_bounds_list, pillar_bounds_list = inner_layout(polygon_bounds, 1)
        inner_layouts += car_bounds_list
        pillar_layouts += pillar_bounds_list

    # 外部排布
    outer_layouts = outer_layout(polygon_input, obstacles)
    car_layouts = inner_layouts + outer_layouts
    if len(car_layouts) > best_num:
        best_num = len(car_layouts)
        best_car_layouts = car_layouts
        pillar_layouts = pillar_layouts

    # print(i, len(car_layouts))
    show_car_and_pillar(
        car_layouts, pillar_layouts, obstacles, (min_x, min_y, max_x, max_y)
    )
    aaaa = 1


if __name__ == "__main__":
    main()
