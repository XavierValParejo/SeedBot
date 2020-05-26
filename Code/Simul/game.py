# -*- coding: utf-8 -*-
import pygame
import numpy as np
from sprites import Mur
from sprites import Robot
from os import path
import sys
import ultrasound_mapping as um
from grid_mapping_for_a_star import OccupancyGridMap
import matplotlib.pyplot as plt
from probabilistic_road_map import ppt
from a_star_pygame import astar

GREEN = (76, 187, 23)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BROWN = (101,67,33)
BLACK  = (  0,   0,   0)

TILESIZE_MAP = 20
TILESIZE_OGM = 10

SPEED = 400
SCREENWIDTH=1200
SCREENHEIGHT=800
SCREENWIDTHMAP=481
SCREENHEIGHTMAP=661
 
grid_row = 50
grid_col = 50

f = "mesures.txt"

xo = 5
yo = 25
xf = 20
yf = 25
xfPixel = 200
yfPixel = 200


class Game:
    def __init__(self, opt):
        pygame.init()
        self.total_col = 0
        self.total_row = 0
        self.map_data = []
        pygame.display.set_caption("SeedBot 2D sim")
        self.clock = pygame.time.Clock()
        self.grid_select = np.zeros((grid_row*20,grid_col*20), dtype = np.int8)
        self.rx_game = []
        self.ry_game = []
        self.ruta_a = []
        self.ruta_ppt = []
        self.itera = 0
        self.ox = []
        self.oy = []
        self.ogm = None
        self.load_map()
        self.load_map_to_np()
        if opt == 1:
            self.screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
        else:
            self.screen = pygame.display.set_mode((SCREENWIDTHMAP,SCREENHEIGHTMAP))
        self.screen.blit(pygame.transform.rotate(self.screen, 270), (0,0))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.load_measures()
    
    def load_map(self):
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    
    def load_measures(self):
        dist, ang = um.read_measures(f)
        mapp = um.map_surroundings(dist)
        self.ogm = um.input_points(mapp)
        rows = self.ogm.data.shape[1]
        cols = self.ogm.data.shape[0]
    
    def load_map_to_np(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '2':
                    self.grid_select[row*20:(row+1)*20,col*20:(col+1)*20] = 1
                    self.ox.extend(range(row*20,(row+1)*20))
                    self.oy.extend(range(col*20,(col+1)*20))
                if tile == '1':
                    self.grid_select[row*20:(row+1)*20,col*20:(col+1)*20] = 2
                    self.ox.extend(range(row*20,(row+1)*20))
                    self.oy.extend(range(col*20,(col+1)*20))
                if tile == '0':
                    self.xo = row*20
                    self.yo = col*20
                self.total_col += 1
            self.total_row += 1
    
    def algo(self, mapp):
        if mapp == 1:    
            route = astar(self.ogm.data, (xo,yo) , (xf,yf))
            route = route
            route = route[::-1]
            self.ruta_a = route
        else:
            ogm = OccupancyGridMap(self.grid_select,1)
            route = astar(self.grid_select, (self.xo,self.yo) , (xfPixel,yfPixel))
            route = route #+ [(self.xo,self.yo)]
            route = route[::-1]
            self.ruta_a = route
            ox,oy,rx,ry = ppt(self.ox, self.oy, self.xo + 1, self.yo + 1, xfPixel,yfPixel)
        return route
    
    def new_sim(self):
        self.all_sprites = pygame.sprite.Group()
        self.murs = pygame.sprite.Group()
        
    def update(self):
        self.all_sprites.update()
                    
    def draw_grid(self, mapp):
        if mapp == 1:
            self.background.fill(GREEN)
            self.load_measures()
            row = self.ogm.data.shape[0]
            col = self.ogm.data.shape[1]
            for x in range(0, row):
                for y in range(0, col):
                    if self.ogm.data[x][y] != 0:
                        Mur(self, y,x, BLACK,mapp)    
        else:
            self.background.fill(GREEN)
            for row, tiles in enumerate(self.map_data):
             for col, tile in enumerate(tiles):
                 if tile == '1':
                     Mur(self, col, row, BROWN,mapp)
                 if tile == '2':
                     Mur(self,col,row, BLACK,mapp)
                 if tile == '0':
                     self.pos_xo = row
                     self.pos_yo = col 
    
    def draw_lines(self, mapp):
        if mapp == 1:    
            for x in range(0, 1024, TILESIZE_OGM):
                pygame.draw.line(self.screen, GREY, (x,0),(x,SCREENHEIGHT))
            for y in range(0,1000,TILESIZE_OGM):
                pygame.draw.line(self.screen, GREY, (0,y),(1024,y))
        else:
            for x in range(0, 1024, TILESIZE_MAP):
                pygame.draw.line(self.screen, GREY, (x,0),(x,SCREENHEIGHTMAP))
            for y in range(0,1000,TILESIZE_MAP):
                pygame.draw.line(self.screen, GREY, (0,y),(1024,y))
            
    def draw(self,mapp):
        self.screen.fill(GREEN)
        self.draw_lines(mapp)
        self.draw_grid(mapp)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
       
    
    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def reconeixement(self):
        x = 0
        while x < 360:
            self.robot.image = pygame.transform.rotate(self.robot.rotate_image,x)
            self.robot.draw(self.screen)
            x +=1
            pygame.display.flip()
            pygame.time.delay(10)
        self.robot.kill()
    
    def run(self, mapp):
        self.playing = True
        if mapp == 1:
            self.robot = Robot(self,RED,xo,yo, mapp)
        else:
            self.robot = Robot(self, RED, self.xo,self.yo,mapp)
        self.reconeixement()
        ruta = 1
        route = self.algo(mapp)
        while self.playing:
            self.draw(mapp)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.playing=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
            Mur(self, self.yo, self.xo, GREEN,mapp)
            self.robot.move(route, self.itera, self.ruta_ppt, ruta)
            self.robot.image = pygame.transform.rotate(self.robot.rotate_image, self.robot.orientacio_x)
            self.robot.draw(self.screen)
            pygame.display.flip()
            if (self.itera <=len(route)-2):
                self.itera += 1
            self.dt = self.clock.tick(60)
                        
mapp = 1    
g = Game(mapp)
while True:
    g.new_sim()
    g.run(mapp)