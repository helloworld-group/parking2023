from typing import Dict
from park_analysis.park_utils import LightArea,Path,Trajectory
import pandas as pd
    
def define_park_areas()-> Dict[str,LightArea]:
    Park_Areas={}
    Park_Areas["A"]=LightArea("A")
    Park_Areas["A"].lighting_num=2
    Park_Areas["B"]=LightArea("B")
    Park_Areas["B"].lighting_num=1
    Park_Areas["C"]=LightArea("C")
    Park_Areas["C"].lighting_num=2
    Park_Areas["D"]=LightArea("D")
    Park_Areas["D"].lighting_num=2
    Park_Areas["E"]=LightArea("E")
    Park_Areas["E"].lighting_num=1
    Park_Areas["F"]=LightArea("F")
    Park_Areas["F"].lighting_num=2
    Park_Areas["G"]=LightArea("G")
    Park_Areas["G"].lighting_num=2
    Park_Areas["H"]=LightArea("H")
    Park_Areas["H"].lighting_num=2
    Park_Areas["I"]=LightArea("I")
    Park_Areas["I"].lighting_num=2
    Park_Areas["J"]=LightArea("J")
    Park_Areas["J"].lighting_num=2
    Park_Areas["K"]=LightArea("K")
    Park_Areas["K"].lighting_num=2
    Park_Areas["L"]=LightArea("L")
    Park_Areas["L"].lighting_num=2
    Park_Areas["M"]=LightArea("M")
    Park_Areas["M"].lighting_num=2
    Park_Areas["N"]=LightArea("N")
    Park_Areas["N"].lighting_num=1
    Park_Areas["O"]=LightArea("O")
    Park_Areas["O"].lighting_num=2
    Park_Areas["P"]=LightArea("P")
    Park_Areas["P"].lighting_num=2
    Park_Areas["Q"]=LightArea("Q")
    Park_Areas["Q"].lighting_num=1
    Park_Areas["R"]=LightArea("R")
    Park_Areas["R"].lighting_num=2
    Park_Areas["S"]=LightArea("S")
    Park_Areas["S"].lighting_num=2
    Park_Areas["T"]=LightArea("T")
    Park_Areas["T"].lighting_num=2
    Park_Areas["U"]=LightArea("U")
    Park_Areas["U"].lighting_num=2
    Park_Areas["V"]=LightArea("V")
    Park_Areas["V"].lighting_num=2
    Park_Areas["W"]=LightArea("W")
    Park_Areas["W"].lighting_num=2
    return Park_Areas
    
def define_road_areas()->Dict[str,LightArea]:
    Road_Areas={}
    Road_Areas["a"]=LightArea("a")
    Road_Areas["a"].lighting_num=4
    Road_Areas["b"]=LightArea("b")
    Road_Areas["b"].lighting_num=2
    Road_Areas["c"]=LightArea("c")
    Road_Areas["c"].lighting_num=2
    Road_Areas["d"]=LightArea("d")
    Road_Areas["d"].lighting_num=4
    Road_Areas["e"]=LightArea("e")
    Road_Areas["e"].lighting_num=4
    Road_Areas["f"]=LightArea("f")
    Road_Areas["f"].lighting_num=4
    Road_Areas["g"]=LightArea("g")
    Road_Areas["g"].lighting_num=4
    Road_Areas["h"]=LightArea("h")
    Road_Areas["h"].lighting_num=4
    Road_Areas["i"]=LightArea("i")
    Road_Areas["i"].lighting_num=4
    Road_Areas["j"]=LightArea("j")
    Road_Areas["j"].lighting_num=4
    Road_Areas["k"]=LightArea("k")
    Road_Areas["k"].lighting_num=4
    Road_Areas["l"]=LightArea("l")
    Road_Areas["l"].lighting_num=4
    Road_Areas["m"]=LightArea("m")
    Road_Areas["m"].lighting_num=4
    Road_Areas["n"]=LightArea("n")
    Road_Areas["n"].lighting_num=4
    Road_Areas["o"]=LightArea("o")
    Road_Areas["o"].lighting_num=4
    return Road_Areas

def define_light_areas()-> Dict[str,LightArea]:
    road_areas=define_road_areas()
    park_areas=define_park_areas()
    light_areas = {**road_areas, **park_areas}
    return light_areas

def read_paths(file_path: str)-> Dict[str,Path]:
    paths={}
    with open(file_path, 'r') as file:
        for line in file:
            # 移除换行符
            line = line.strip()
            
            # 使用逗号分割每一行的数据
            data = line.split(',')
            
            parking_id=str(data[0])
            paths[parking_id]=Path(parking_id)
            
            for i in range(1,len(data)):
                paths[parking_id].add_area_id(str(data[i]))
    return paths

def define_trajectory(file_path:str)->Dict[str,Trajectory]:
    trajectorys={}
    df = pd.read_csv(file_path)
    # 遍历每一行
    for index, row in df.iterrows():
        vehicle_id = row['vehicle_id']
        path_id = row['path_id']
        time = row['time']
        trajectorys[str(vehicle_id)]=Trajectory(trajectory_id=str(vehicle_id),path_id=str(path_id),start_time=str(time))
        
    return trajectorys