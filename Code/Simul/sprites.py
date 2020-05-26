# -*- coding: utf-8 -*-
import pygame
import math
import numpy as np

BLACK  = (0,0,0)
TILESIZE = 20
BROWN = (101,67,33)

class Mur(pygame.sprite.Sprite):
    def __init__(self, game, y,x,color, opt):
        self.groups = game.all_sprites, game.murs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        if opt == 1:
            tile = 10
        else:
            tile = 20
        self.rect.x = x * tile
        self.rect.y = y * tile


class Robot(pygame.sprite.Sprite):
    def __init__(self,game, color, x, y,opt):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.image.load("sprite2.png", "True")
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rotate_image = self.image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        if opt == 1:
            tile = 9
        else:
            tile = 15
        self.rect.x = x * tile - 1
        self.rect.y = y * tile - 1
        self.ruta = []
        self.iter = None
        self.orientacio_x = 0
        self.orientacio_y = 0
        self.orientacio = math.sqrt(math.pow(self.orientacio_x,2) + math.pow(self.orientacio_y,2))
        
    
    def move(self, ruta2, itera, ruta_ppt, opcio):
        aux_x = self.x
        aux_y = self.y
        if opcio == 1:
            self.ruta = ruta2
            dir_x = self.x - self.ruta[itera][0]
            dir_y = self.y - self.ruta[itera][1]
            self.x = self.ruta[itera][0]
            self.y = self.ruta[itera][1]
        else:
            self.ruta = ruta_ppt
            self.x = ruta_ppt[itera][0]
            self.y = ruta_ppt[itera][1]
        
        if aux_x < self.x and aux_y < self.y:
            self.orientacio_x = -45#diagonal inferior dreta SE
        if aux_x > self.x and aux_y > self.y:
            self.orientacio_x = 135 #diagona superior esquerra NO
        if aux_x < self.x and aux_y < self.y:
            self.orientacio_x = -135 #SO
        if aux_x < self.x and aux_y > self.y:
            self.orientacio_x = 45 #NE
        if aux_x < self.x and aux_y == self.y:
            self.orientacio_x = 0 #E
        if aux_x > self.x and aux_y == self.y:
            self.orientacio_x = 180 #O
        if aux_x == self.x and aux_y < self.y:
            self.orientacio_x = -90 #S
        if aux_x == self.x and aux_y > self.y:
            self.orientacio_x = 90 #N
    
    def change_image(self):
        self.image = pygame.image.load("143206.png", "True")
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
    
    def draw(self, surface):
        surface.blit(self.image,(self.x*TILESIZE,self.y*TILESIZE))
    
    def destroy(self):
        self.image.kill()
    
    