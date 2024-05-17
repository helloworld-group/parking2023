from park_analysis_setting import *
from typing import Dict,List
from datetime import datetime, timedelta

def calculate_consumption(light_areas):
    total_consumption=0
    total_time=0
    for key,light_area in light_areas.items():
        time=light_area.calculate_time()
        # print("area:"+key)
        # print("time:"+str(time))
        total_time+=time
        consumption=light_area.calculate_time()*light_area.lighting_num
        total_consumption+=light_area.calculate_time()*light_area.lighting_num
    print("total consumption:",total_consumption)

def main():
    light_areas=define_light_areas()
    road_areas=define_road_areas()
    park_areas=define_park_areas()
    paths=read_paths("path_leading.txt")
    trajectorys=define_trajectory("parking_enter_scheme_leading.csv")
    # paths=read_paths("path_booking.txt")
    # trajectorys=define_trajectory("parking_enter_scheme_booking.csv")
    for key,trajectory in trajectorys.items():
        light_areas=trajectory.calculate_period(paths=paths,light_areas=light_areas)
        road_areas=trajectory.calculate_period(paths=paths,light_areas=road_areas)
        park_areas=trajectory.calculate_period(paths=paths,light_areas=park_areas)
        
    calculate_consumption(light_areas)
    calculate_consumption(road_areas)
    calculate_consumption(park_areas)

if __name__ == "__main__":
    main()