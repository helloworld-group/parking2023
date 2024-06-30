import csv
import pandas as pd
from typing import Dict,List
from datetime import datetime, timedelta
from motion_planning.map_tools import Node,Light,Map
# from park_analysis.park_analysis_setting import *


class VehicleSchedule():
    def __init__(self,id:int,target_id:int,time,entrance_id: int,exit_id:int):
        self.id=id
        self.target_id=target_id
        self.entrance_id=entrance_id
        self.exit_id=exit_id
        self.start_time=parse_time(time)
        self.lighting_delay_time_minute=get_lighting_delay_time_minute(self.start_time) #分钟
        
        aaa=1


    def calculate_light_periods(self,start_time:datetime,path: List[Node],lights:Dict[int,Light]):
        for idx in range(len(path)-1):
            # select the lights which are activated by the path
            for light_id,light in lights.items():
                if light.is_activated_by_path_section(path[idx],path[idx+1],threshold=5):
                    lights[light_id].add_period(start_time,start_time+timedelta(minutes=self.lighting_delay_time_minute))
        return lights
    
    def calculate_park_light_periods(self,end_node:Node,start_time:datetime,lights:Dict[int,Light]):
        # end_node=map.weighted_graph.nodes[]      self.target_id
        for light_id,light in lights.items():
            if light.is_activated_by_node(end_node,threshold=4):
                lights[light_id].add_period(start_time,start_time+timedelta(minutes=self.lighting_delay_time_minute))
                break
        return lights
        
def read_schedule(csv_file:str)->Dict[int,VehicleSchedule]:
    vehicle_schedules:Dict[int,VehicleSchedule]={}
    df = pd.read_csv(csv_file)
    # 遍历每一行
    for index, row in df.iterrows():
        vehicle_id = int(row['vehicle_id'])
        target_id = int(row['target_id'])
        time = row['time']
        entrance_id = int(row['entrance_id'])
        exit_id=int(row['exit_id'])
        vehicle_schedule=VehicleSchedule(vehicle_id,target_id,time,entrance_id,exit_id)
        vehicle_schedules[vehicle_id]=vehicle_schedule
    return vehicle_schedules

class LightArea:
    def __init__(self, name:str):
        self.lighting_periods=[]
        self.lighting_num=0
    
    def add_period(self,time_start:int,time_end:int):
        self.lighting_periods.append([time_start,time_end])
    
    def merge_period(self):
        self.lighting_periods.sort(key=lambda x:x[0])
        result=[]
        if len(self.lighting_periods)==0:
            return
        
        result.append(self.lighting_periods[0])
        for i in range(1,len(self.lighting_periods)):
            if result[-1][1]>=self.lighting_periods[i][0]:
                result[-1][1]=max(result[-1][1],self.lighting_periods[i][1])
            else:
                result.append(self.lighting_periods[i])
        self.lighting_periods=result
        
    def calculate_time(self)-> int:
        self.merge_period()
        time=0
        for period in self.lighting_periods:
            time+=calculate_time_difference(period[1],period[0])
        return time

class Path:
    def __init__(self, parking_target: str):
        self.parking_target=parking_target
        self.areas=[]
    def add(self,area_ids: list):
        for id in area_ids:
            self.areas.append(id)
    def add_area_id(self,area_id:str):
        self.areas.append(area_id)
            
class Trajectory:
    def __init__(self, trajectory_id, path_id,start_time):
        self.trajectory_id=trajectory_id
        self.path_id=path_id
        self.start_time=parse_time(start_time)
        self.lighting_delay_time_minute=get_lighting_delay_time_minute(self.start_time) #分钟
        
    # calculate the occupied time for all the related light areas
    def calculate_period(self,paths:Dict[str, Path],light_areas: Dict[str,LightArea]):
        path=paths[self.path_id]
        for area in path.areas:
            if area in light_areas:
                light_areas[area].add_period(self.start_time,self.start_time+timedelta(minutes=self.lighting_delay_time_minute))
        return light_areas

def parse_time(time_str):
    # 时间字符串格式为 "H:M"
    time_format = "%H:%M"
    # 使用 strptime 函数将字符串解析为 datetime 对象
    time_obj = datetime.strptime(time_str, time_format)
    return time_obj
# calculate the difference between two times in minutes
def calculate_time_difference(time1, time2):
    # 计算时间差
    time_diff = abs(time1 - time2)
    # 转换为分钟
    time_diff_minutes = time_diff.total_seconds() / 60
    return time_diff_minutes



def get_lighting_delay_time_minute(time:datetime)-> int:
    time1=parse_time("6:00")
    time2=parse_time("8:00")
    time3=parse_time("9:30")
    time4=parse_time("12:00")
    
    time5=parse_time("17:00")
    time6=parse_time("18:30")
    time7=parse_time("20:00")
    time8=parse_time("0:00")
    if time>=time1 and time<time2:
        return 3
    elif time>=time2 and time<time3 :
        return 5
    elif time>=time3 and time<=time4 :
        return 3
    
    elif time>=time5 and time<time6 :
        return 5

    elif time>=time6 and time<time7 :
        return 3
    
    elif time>=time7 and time<=time8 :
        return 3
    
    else:
        return 3