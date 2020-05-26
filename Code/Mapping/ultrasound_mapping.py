import numpy as np
import matplotlib.pyplot as plt
import math
import lidar_to_grid_map as lg
from grid_mapping_for_a_star import OccupancyGridMap
from a_star_for_ogm_testing import a_star

f = "mesures.txt"

def read_measures(file):
    measures = [line.split(",") for line in open(file)]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    ang = np.array(angles)
    dist = np.array(distances)
    return dist,ang

def map_surroundings(dist):
    xyreso = 0.02  # x-y grid resolution
    yawreso = math.radians(3.1)  # yaw angle resolution [rad]
    ox = np.sin(ang) * dist
    oy = np.cos(ang) * dist
    pmap, minx, maxx, miny, maxy, xyreso = lg.generate_ray_casting_grid_map(ox, oy, xyreso, False)
    xyres = np.array(pmap).shape
    return pmap

def input_points(pmap):
    for x in dist:
        x = x / 10
    ogm = OccupancyGridMap(pmap, 1)
    path, path_idx = a_star((25,30), (50,40),ogm)
    xPath, yPath = zip(*path)
    return ogm

dist, ang = read_measures(f)
mapp = map_surroundings(dist)
tipus_=input_points(mapp)