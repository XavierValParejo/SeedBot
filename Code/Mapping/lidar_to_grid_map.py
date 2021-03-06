"""
LIDAR to 2D grid map example
author: Erno Horvath, Csaba Hajdu based on Atsushi Sakai's scripts (@Atsushi_twi)
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

EXTEND_AREA = 1.0


def file_read(f):
    """
    Reading LIDAR laser beams (angles and corresponding distance data)
    """
    measures = [line.split(",") for line in open(f)]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances


def bresenham(start, end):
    """
    Implementation of Bresenham's line drawing algorithm
    See en.wikipedia.org/wiki/Bresenham's_line_algorithm
    Bresenham's Line Algorithm
    Produces a np.array from start and end (original from roguebasin.com)
    >>> points1 = bresenham((4, 4), (6, 10))
    >>> print(points1)
    np.array([[4,4], [4,5], [5,6], [5,7], [5,8], [6,9], [6,10]])
    """
    # setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx) # determine how steep the line is
    if is_steep: # rotate line
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False # swap start and end points if necessary and store swap state
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1 # recalculate differentials
    dy = y2 - y1 # recalculate differentials
    error = int(dx / 2.0) # calculate error
    ystep = 1 if y1 < y2 else -1
    # iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = [y, x] if is_steep else (x, y)
        points.append(coord)   
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if swapped: # reverse the list if the coordinates were swapped
        points.reverse()
    points = np.array(points)
    return points


def calc_grid_map_config(ox, oy, xyreso):
    """
    Calculates the size, and the maximum distances according to the the measurement center
    """
    minx = round(min(ox) - EXTEND_AREA / 2.0)
    miny = round(min(oy) - EXTEND_AREA / 2.0)
    maxx = round(max(ox) + EXTEND_AREA / 2.0)
    maxy = round(max(oy) + EXTEND_AREA / 2.0)
    xw = int(round((maxx - minx) / xyreso))
    yw = int(round((maxy - miny) / xyreso))
    #print("The grid map is ", xw, "x", yw, ".")
    return minx, miny, maxx, maxy, xw, yw


def atan_zero_to_twopi(y, x):
    angle = math.atan2(y, x)
    if angle < 0.0:
        angle += math.pi * 2.0
    return angle


def init_floodfill(cpoint,  opoints, xypoints, mincoord, xyreso):
    """
    cpoint: center point
    opoints: detected obstacles points (x,y)
    xypoints: (x,y) point pairs
    """
    centix, centiy = cpoint
    prev_ix, prev_iy = centix - 1, centiy
    ox, oy = opoints
    xw, yw = xypoints
    minx, miny = mincoord
    pmap = (np.ones((xw, yw))) * 0.5
    for (x, y) in zip(ox, oy):
        ix = int(round((x - minx) / xyreso))  # x coordinate of the the occupied area
        iy = int(round((y - miny) / xyreso))  # y coordinate of the the occupied area
        free_area = bresenham((prev_ix, prev_iy), (ix, iy))
        for fa in free_area:
            pmap[fa[0]][fa[1]] = 0  # free area 0.0
        prev_ix = ix
        prev_iy = iy
    return pmap


def flood_fill(cpoint, pmap):
    """
    cpoint: starting point (x,y) of fill
    pmap: occupancy map generated from Bresenham ray-tracing
    """
    # Fill empty areas with queue method
    sx, sy = pmap.shape
    fringe = deque()
    fringe.appendleft(cpoint)
    while fringe:
        n = fringe.pop()
        nx, ny = n
        # West
        if nx > 0:
            if pmap[nx - 1, ny] == 0.5:
                pmap[nx - 1, ny] = 0.0
                fringe.appendleft((nx - 1, ny))
        # East
        if nx < sx - 1:
            if pmap[nx + 1, ny] == 0.5:
                pmap[nx + 1, ny] = 0.0
                fringe.appendleft((nx + 1, ny))
        # North
        if ny > 0:
            if pmap[nx, ny - 1] == 0.5:
                pmap[nx, ny - 1] = 0.0
                fringe.appendleft((nx, ny - 1))
        # South
        if ny < sy - 1:
            if pmap[nx, ny + 1] == 0.5:
                pmap[nx, ny + 1] = 0.0
                fringe.appendleft((nx, ny + 1))


def generate_ray_casting_grid_map(ox, oy, xyreso, breshen=True):
    """
    The breshen boolean tells if it's computed with bresenham ray casting (True) or with flood fill (False)
    """
    minx, miny, maxx, maxy, xw, yw = calc_grid_map_config(ox, oy, xyreso)
    pmap = np.ones((xw, yw))/2 # default 0.5 -- [[0.5 for i in range(yw)] for i in range(xw)] 
    centix = int(round(-minx / xyreso)) # center x coordinate of the grid map
    centiy = int(round(-miny / xyreso)) # center y coordinate of the grid map
    # occupancy grid computed with bresenham ray casting
    if breshen:
        for (x, y) in zip(ox, oy):
            ix = int(round((x - minx) / xyreso)) # x coordinate of the the occupied area
            iy = int(round((y - miny) / xyreso)) # y coordinate of the the occupied area
            laser_beams = bresenham((centix, centiy), (ix, iy)) # line form the lidar to the cooupied point
            for laser_beam in laser_beams:
                pmap[laser_beam[0]][laser_beam[1]] = 0.0 # free area 0.0
            pmap[ix][iy] = 1.0     # occupied area 1.0
            pmap[ix+1][iy] = 1.0   # extend the occupied area
            pmap[ix][iy+1] = 1.0   # extend the occupied area
            pmap[ix+1][iy+1] = 1.0 # extend the occupied area
    # occupancy grid computed with with flood fill
    else:
        pmap = init_floodfill((centix, centiy), (ox, oy), (xw, yw),  (minx, miny), xyreso)
        flood_fill((centix, centiy), pmap)
        pmap = np.array(pmap, dtype=np.float)
        for (x, y) in zip(ox, oy):
            ix = int(round((x - minx) / xyreso))
            iy = int(round((y - miny) / xyreso))
            pmap[ix][iy] = 1.0     # occupied area 1.0
            #pmap[ix+1][iy] = 1.0   # extend the occupied area
            pmap[ix][iy+1] = 1.0   # extend the occupied area
            #pmap[ix+1][iy+1] = 1.0 # extend the occupied area
    return pmap, minx, maxx, miny, maxy, xyreso