import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from typing import List
from matplotlib import patches
import shapely
import os
def show_polygon(polygon):
    p = gpd.GeoSeries(polygon)
    p.plot()
    plt.show()

def save_description(road_width: float,folder: str,text_name: str):
    folder=folder.rstrip("\\")
    if not os.path.exists(folder):
        os.makedirs(folder) 
    description="road_width:"+str(road_width)
    text_name+='.txt'
    path=os.path.join(folder,text_name)
    with open(path, "w", encoding="utf-8") as file:
        # 将字符串写入文件
        file.write(description)

def save_polygon(polygon: Polygon,folder:str="parking_layout_data",img_name: str="text.jpg"):
    folder=folder.rstrip("\\")
    if not os.path.exists(folder):
        os.makedirs(folder) 
    # p = gpd.GeoSeries(polygon)
    # p.plot(facecolor="green")

    x_exterior, y_exterior = polygon.exterior.xy
    # 提取内部空洞的坐标
    x_hole, y_hole = [], []
    for interior in polygon.interiors:
        x_interior, y_interior = interior.xy
        x_hole.extend(x_interior)
        y_hole.extend(y_interior)
    fig, ax = plt.subplots()
    # 绘制外部多边形
    ax.fill(x_exterior, y_exterior, 'lightblue', label='Exterior')

    # 绘制内部空洞
    ax.fill(x_hole, y_hole, 'red', label='Hole')
    # plt.show()


    # p.plot(facecolor="green")
    # if obstacle:
    #     p2=gpd.GeoSeries(obstacle)
    #     p2.plot(facecolor="red")
    path=os.path.join(folder,img_name)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_aspect("equal", adjustable="box")
    plt.savefig(path,bbox_inches='tight',dpi=100)
    plt.close()

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

def show_layouts(layouts: List[tuple], axis_range):
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


def show_car_and_pillar(car, pillar, obstacle:Polygon,axis_range,folder="parking_generate_data/",img_name="test.jpg",save_mode=False):
    fig, ax = plt.subplots()
    # ax.set_xlim(axis_range[0], axis_range[2])
    # ax.set_ylim(axis_range[1], axis_range[3])
    for bounds in car:
        min_x, min_y, max_x, max_y = bounds
        ax.plot(
            [min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y],
            color="black",
            # linewidth=0.5,
            linewidth=2.0,
        )
        rectangle = patches.Rectangle(
            (min_x, min_y),
            max_x - min_x,
            max_y - min_y,
            linewidth=2.0,
            edgecolor="black",
            facecolor="lime",
        )
        ax.add_patch(rectangle)
    for bounds in pillar:
        min_x, min_y, max_x, max_y = bounds
        ax.plot(
            [min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y],
            color="red",
            linewidth=0.5,
        )
    x_exterior, y_exterior = obstacle.exterior.xy
    ax.fill(x_exterior, y_exterior, 'red', label='Exterior')

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    # 保持xy比例一致
    ax.set_aspect("equal", adjustable="box")
    # plt.xlabel("X Axis")
    # plt.ylabel("Y Axis")
    # plt.title("Rectangles Plot")
    # plt.grid(True)
    folder=folder.rstrip("\\")
    if not os.path.exists(folder):
        os.makedirs(folder) 
    path=os.path.join(folder,img_name)
    if save_mode:
        plt.savefig(path,bbox_inches='tight',dpi=100)
    else:
        plt.show()
    plt.close()