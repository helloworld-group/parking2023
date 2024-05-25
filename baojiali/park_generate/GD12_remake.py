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
from util import *
from map import *


class CFG:
    rand_times = 2  # 随机次数上线
    min_size = 0.2  # 拓展精度
    min_area_rate = 0.01
    eps = 1e-6
    car_width = 2.4  # 车宽度
    car_length = 5.4  # 车长度
    pillar_width = 0.4  # 柱子宽度
    pillar_length = 0.8  # 柱子长度
    road_width = 6.5  # 道路宽度
    car_group_limit = 4  # 车道组数


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
                polygon = polygon.difference(input_polygons_list[i])
    return polygon


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


def maximum_cut_polygon(polygon: Polygon):
    repeat_times = 10
    ret_list = []
    min_x, min_y, max_x, max_y = polygon.bounds
    origin_area = polygon.area
    while polygon.area > origin_area * CFG.min_area_rate:
        cur_times = 0
        max_polygon_area = 0
        max_polygon = None
        max_start_x, max_start_y, max_end_x, max_end_y = 0, 0, 0, 0
        while True:
            if cur_times > repeat_times:
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
        polygon = polygon.difference(max_polygon)
        ret_list.append((max_start_x, max_start_y, max_end_x, max_end_y))
    return ret_list
    pass


def inner_layout(polygon_bounds: tuple, layout_type: int):
    car_bounds_list = []
    pillar_bounds_list = []
    min_x, min_y, max_x, max_y = polygon_bounds
    car_width = CFG.car_width
    car_length = CFG.car_length
    min_x, min_y, max_x, max_y = (
        min_x + CFG.road_width / 2,
        min_y + CFG.road_width / 2,
        max_x - CFG.road_width / 2,
        max_y - CFG.road_width / 2,
    )
    if layout_type == 1:
        count_num_i = 0
        i = min_x
        while i < max_x - car_width:
            count_num_i += 1
            count_num_j = 0
            j = min_y
            while j < max_y - car_length:
                count_num_j += 1
                if count_num_i % 4 == 1 and count_num_j % 2 == 1:
                    if count_num_j == 1 and count_num_i == 1:
                        i += CFG.pillar_width
                    pillar_bounds_list.append(
                        (i - CFG.pillar_width, j, i, j + CFG.pillar_length)
                    )
                    if j + car_length < max_y:
                        pillar_bounds_list.append(
                            (
                                i - CFG.pillar_width,
                                j + car_length - CFG.pillar_length / 2,
                                i,
                                j + car_length + CFG.pillar_length / 2,
                            )
                        )
                    if j + car_length * 2 < max_y:
                        pillar_bounds_list.append(
                            (
                                i - CFG.pillar_width,
                                j + car_length * 2 - CFG.pillar_length,
                                i,
                                j + car_length * 2,
                            )
                        )
                car_bounds_list.append([i, j, i + car_width, j + car_length])
                if (
                    count_num_i % 4 == 0 or i + car_width * 2 > max_x
                ) and count_num_j % 2 == 1:
                    i += CFG.pillar_width
                    pillar_bounds_list.append(
                        (
                            i + car_width - CFG.pillar_width,
                            j,
                            i + car_width,
                            j + CFG.pillar_length,
                        )
                    )
                    if j + car_length < max_y:
                        pillar_bounds_list.append(
                            (
                                i + car_width - CFG.pillar_width,
                                j + car_length - CFG.pillar_length / 2,
                                i + car_width,
                                j + car_length + CFG.pillar_length / 2,
                            )
                        )
                    if j + car_length * 2 < max_y:
                        pillar_bounds_list.append(
                            (
                                i + car_width - CFG.pillar_width,
                                j + car_length * 2 - CFG.pillar_length,
                                i + car_width,
                                j + car_length * 2,
                            )
                        )
                    i -= CFG.pillar_width
                if count_num_j % 2 == 0:
                    j += CFG.road_width
                j += car_length
            if count_num_i % 4 == 0:
                i += CFG.pillar_width
            if count_num_i % (4 * CFG.car_group_limit) == 0:
                i += CFG.road_width
            i += car_width
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


def outer_layout(polygon):
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
    for i in range(len(ex_points)):
        cur_point = np.array(ex_points[i])
        next_point = np.array(ex_points[(i + 1) % len(ex_points)])
        next_next_point = np.array(ex_points[(i + 2) % len(ex_points)])
        pre_point = np.array(ex_points[(i - 1) % len(ex_points)])
        line1 = next_point - cur_point
        line2 = pre_point - cur_point

        concavity_cur = judge_concavity(pre_point, cur_point, next_point)
        concavity_next = judge_concavity(cur_point, next_point, next_next_point)
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
    for car_layout in car_layouts:
        min_x, min_y, max_x, max_y = car_layout
        cur_polygon = cur_polygon.union(
            Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
        )
    # show_polygon(cur_polygon)

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


def generate_random_obstacle(
    layout_buffer: Polygon = None, w_base=20, h_base=20,noise_w=0,noise_h=0
) -> Polygon:
    min_x, min_y, max_x, max_y = layout_buffer.bounds
    for i in range(100):
        center_x = random.randint(int(min_x), int(max_x))
        center_y = random.randint(int(min_y), int(max_y))

        # noise_w = 0
        # noise_h = 0
        width = w_base + noise_w
        height = h_base + noise_h
        obstacle_input_list = []
        obstacle_input_list.append((center_x - width / 2, center_y - height / 2))
        obstacle_input_list.append((center_x - width / 2, center_y + height / 2))
        obstacle_input_list.append((center_x + width / 2, center_y + height / 2))
        obstacle_input_list.append((center_x + width / 2, center_y - height / 2))
        obstacle_polygon = Polygon(obstacle_input_list)
        if obstacle_polygon.within(layout_buffer):
            return obstacle_polygon
    return None


def generate_outline(mode_variant_layout=False, w=100, h=100) -> List:
    input_points_list = []
    if mode_variant_layout:
        direction = random.choice([0, 1, 2, 3])  # 随机决定中心点产生的缺口的方向
        if direction == 0:  # 缺口在左上角
            x_rand = random.randint(30, w / 2)  # random x position
            y_rand = random.randint(h / 2, h - 30)  # random x position
            input_points_list.append((0, 0))
            input_points_list.append((0, y_rand))
            input_points_list.append((x_rand, y_rand))
            input_points_list.append((x_rand, h))
            input_points_list.append((w, h))
            input_points_list.append((w, 0))
        elif direction == 1:  # 缺口在右上角
            x_rand = random.randint(w / 2, w - 30)  # random x position
            y_rand = random.randint(h / 2, h - 30)  # random x position
            input_points_list.append((0, 0))
            input_points_list.append((0, h))
            input_points_list.append((x_rand, h))
            input_points_list.append((x_rand, y_rand))
            input_points_list.append((w, y_rand))
            input_points_list.append((w, 0))
        elif direction == 2:  # 缺口在右下角
            x_rand = random.randint(w / 2, w - 30)  # random x position
            y_rand = random.randint(h / 2, h - 30)  # random x position
            input_points_list.append((0, 0))
            input_points_list.append((0, h))
            input_points_list.append((w, h))
            input_points_list.append((w, y_rand))
            input_points_list.append((x_rand, y_rand))
            input_points_list.append((x_rand, 0))
        elif direction == 3:  # 缺口在左下角
            x_rand = random.randint(30, w / 2)  # random x position
            y_rand = random.randint(h / 2, h - 30)  # random x position
            input_points_list.append((0, y_rand))
            input_points_list.append((0, h))
            input_points_list.append((w, h))
            input_points_list.append((w, 0))
            input_points_list.append((x_rand, 0))
            input_points_list.append((x_rand, y_rand))
    else:
        input_points_list.append((0, 0))
        input_points_list.append((0, h))
        input_points_list.append((w, h))
        input_points_list.append((w, 0))
    return input_points_list


def generate_random_layout() -> List[Polygon]:
    w_base = 150  # basic width
    h_base = 150  # basic height
    noise_h = random.randint(-5, 5)  # noise of height
    noise_w = random.randint(-5, 5)  # noise of width

    noise_h = 0  # set noise of height to 0 to simply the polygon
    noise_w = 0  # set noise of width to 0 to simply the polygon
    w = w_base + noise_w
    h = h_base + noise_h
    layout_points_list = []  # the point of the polygon, counter clockswise
    mode_variant_layout = True
    layout_points_list = generate_outline(
        mode_variant_layout=mode_variant_layout, w=w, h=h
    )

    layout_polygon = Polygon(layout_points_list)

    polygon_buffer = buffer(
        layout_polygon, -CFG.car_length - CFG.road_width / 2, join_style="mitre"
    )
    mode_obstacle = True
    if mode_obstacle:
        obstacle = generate_random_obstacle(
            layout_buffer=polygon_buffer,
            w_base=20,
            h_base=20,
            noise_w = random.randint(-5, 10),
            noise_h = random.randint(-5, 10)
        )
        layout_polygon = layout_polygon.difference(obstacle)
    else:
        obstacle = []
    return layout_polygon, obstacle


def generate_data(
    layout_folder: str = "parking_layout_data",
    generate_folder: str = "parking_generate_data",
    text_folder:str="parking_description_data",
    name: str = "001",
    random_params: bool = False,
):

    if random_params:
        random_road_width = random.choice([4.5, 8.5])
        CFG.road_width=random_road_width
        save_description(CFG.road_width,text_folder,name)
        
    
    img_name=name+".jpg"
    polygon_input, obstacle = generate_random_layout()
    # polygon_input = polygon_input = read_input("GD12-input.txt")
    min_x, min_y, max_x, max_y = polygon_input.bounds
    # show_polygon(polygon_input)
    save_polygon(polygon=polygon_input, folder=layout_folder, img_name=img_name)

    polygon_input_buffer = buffer(
        polygon_input, -CFG.car_length - CFG.road_width / 2, join_style="mitre"
    )

    # show_polygon(polygon_input_buffer)
    best_num = 0
    best_car_layouts = []
    best_pillar_layouts = []

    # 矩形切割
    # for i in range(CFG.rand_times):
    polygon_bounds_list = maximum_cut_polygon(polygon_input_buffer)
    # show_layouts(polygon_bounds_list, (min_x, min_y, max_x, max_y))
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
    outer_layouts = outer_layout(polygon_input)
    car_layouts = inner_layouts + outer_layouts
    if len(car_layouts) > best_num:
        best_num = len(car_layouts)
        best_car_layouts = car_layouts
        pillar_layouts = pillar_layouts

    # print(i, len(car_layouts))
    show_car_and_pillar(
        car=car_layouts,
        pillar=pillar_layouts,
        obstacle=obstacle,
        axis_range=(min_x, min_y, max_x, max_y),
        folder=generate_folder,
        img_name=img_name,
        save_mode=True,
    )


def main():
    # training data
    for i in range(4000):
        print("data:", i)
        name = "%05d" % i
        generate_data(
            layout_folder="parking_layout_data",
            generate_folder="parking_generate_data",
            description_folder="parking_text_data",
            name=name,
            random_params=True
        )

    # validation data
    for i in range(200):
        print("val:", i)
        name = "%05d" % i
        generate_data(
            layout_folder="val_parking_layout_data",
            generate_folder="val_parking_generate_data",
            description_folder="val_parking_text_data",
            name=name,
            random_params=True
        )

    # test data
    for i in range(200):
        print("test:", i)
        name = "%05d" % i
        generate_data(
            layout_folder="test_parking_layout_data",
            generate_folder="test_parking_generate_data",
            description_folder="test_parking_text_data",
            name=name,
            random_params=True
        )


if __name__ == "__main__":
    main()
