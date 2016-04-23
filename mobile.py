#!/usr/bin/python3

import pygame
import math
import random
from pygame.locals import *
from attacks import *

#This is the parent class which handles any Mobile monster or player type
#activities
class Mobile(pygame.sprite.DirtySprite):
    
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y,image_files):
        super().__init__();

        self.dirty = 2
        self.layer = 2
        mob_choice = image_files[random.randint(0,len(image_files)-1)]
        self.image = pygame.image.load(mob_choice).convert()
        self.ranged_attack_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.level = 1
        self.mob_type_mod = 1
        self.exp = 0
        self.stats = {'HP':self.mob_type_mod *random.randrange(self.level*3,self.level*5),
                      'MP':self.mob_type_mod * random.randrange(self.level*1,self.level*2),
                      'Exp':self.exp,
                      'Level':self.level}
        self.speed = 2
        #This image is typically way too big
        #self.image = pygame.transform.scale(self.image, (self.image.get_width()//2,self.image.get_height()//2))
        
        arrayTest = []
        pixArray = pygame.PixelArray(self.image)
        for index,row in enumerate(pixArray):
            for item in row:
                if item != self.image.map_rgb((255,0,255)):
                    arrayTest.append(index)
        
        arrayTest = list(set(arrayTest))
        pixArray = pixArray[arrayTest[0]:arrayTest[-1],arrayTest[0]:arrayTest[-1]]

        self.image = pixArray.make_surface()
        self.image.set_colorkey(pygame.Color(255, 0, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_r = self.mask
        self.image_r = self.image
        self.image = pygame.transform.flip(self.image,True,False)
        self.image_l = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_l = self.mask
        self.r_attack_images = []
        self.ranged_item = 0
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        #These are for animations
        self.direction = "R"
        self.directions = {'R':self.image_r,'L':self.image_l}
        #These are for attacks
        self.attack_d = {'R':(1,0),'L':(-1,0),'U':(0,-1),'D':(0,1),
                         'RU':(1,-1),'RD':(1,1),'LU':(-1,-1),'LD':(-1,1)}
        self.attack_now_d = 'R'
        self.r_image_d = {'U':0,'RU':1,'R':2,'RD':3,'D':4,'LD':5,'L':6,'LU':7}
        self.mask_dict = {'R':self.mask_r,'L':self.mask_l}

        self.view_port = 100
        self.pathing = False
        self.path_start = False
        self.a_path = []
        self.new_pos = (0,0)
        self.to_square = (0,0)

        self.mob_type = 'M'
        
    def changespeed(self,x,y):
        if(x > 0):
            self.direction = "R"
            if y == 0:
                self.attack_now_d = 'R'
        elif(x < 0):
            self.direction = "L"
            if y == 0:
                self.attack_now_d = 'L'
                
        if y > 0 and x > 0:
            self.attack_now_d = 'RD'
        elif y > 0 and x == 0:
            self.attack_now_d = 'D'
        elif y > 0 and x < 0:
            self.attack_now_d = 'LD'
        elif y < 0 and x == 0:
            self.attack_now_d = 'U'
        elif y < 0 and x < 0:
            self.attack_now_d = 'LU'
        elif y < 0 and x > 0:
            self.attack_now_d = 'RU'
            
        if(math.fabs(self.change_x + x) <= self.speed):
            self.change_x += x

        if(math.fabs(self.change_y + y) <= self.speed):
            self.change_y += y
            

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def set_all_sprites(self,all_sprites):
        self.all_sprites = all_sprites
            
    def move(self, walls,mobiles):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False,collided = pygame.sprite.collide_mask)
        
        mobile_hit_list = pygame.sprite.spritecollide(self, mobiles, False,collided = pygame.sprite.collide_mask)

        if self in mobile_hit_list:
            mobile_hit_list.remove(self)


        if block_hit_list or mobile_hit_list:
            self.rect.x -= self.change_x
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False, collided = pygame.sprite.collide_mask)
        mobile_hit_list = pygame.sprite.spritecollide(self, mobiles, False,collided = pygame.sprite.collide_mask)

        if self in mobile_hit_list:
            mobile_hit_list.remove(self)

                
        if block_hit_list or mobile_hit_list:
            self.rect.y -= self.change_y
        return (self.rect.x,self.rect.y)

    #part of pathfinding
    def follow_path(self,path,map_pix,to_pos):
        self.pathing = True
        self.path_start = True
        self.a_path = path
        self.new_pos = to_pos

    #Part of pathfinding
    def is_moving(self,map_pix):
        if self.pathing:
            if self.path_start:
                try:
                    self.to_square = self.a_path.pop()
                except IndexError:
                    self.stop()
                    self.pathing = False
                    return None
                self.path_start = False
            path_check = [int(math.fabs(x - y)) for x,y in zip(self.get_pos(),self.to_square)]
            if(self.to_square[0] == self.rect.x):
                self.changespeed(0,0)
            elif(self.to_square[0] < self.rect.x):
                self.changespeed(-2,0)
            elif(self.to_square[0] > self.rect.x):
                self.changespeed(2,0)

            if(self.to_square[1] == self.rect.y):
                self.changespeed(0,0)
            elif(self.to_square[1] > self.rect.y):
                self.changespeed(0,2)
            elif(self.to_square[1] < self.rect.y):
                self.changespeed(0,-2)
                
            if path_check[0] <= 2 and path_check[1] <= 2:
                try:
                    self.to_square = self.a_path.pop()
                except IndexError:
                    self.stop()
                    self.pathing = False
                    return None

            goal_check = [int(math.fabs(x - y)) for x,y in zip(self.get_pos(),self.new_pos)]
            if goal_check[0] < 20 and goal_check[1] < 20:
                self.stop()
                self.pathing = False
            
    def group_add(self,group):
        group.add(self)
        group.change_layer(self,2)
        


    def update(self, add_x = None, add_y = None):
        self.dirty = 1
        self.image = self.directions[self.direction]
        self.mask = self.mask_dict[self.direction]
        
            
        if add_x != None and add_y != None:
            self.rect.x -= add_x
            self.rect.y -= add_y

    def get_pos(self):
        return (self.rect.x,self.rect.y)

    def set_mob_type(self,m_type):
        self.mob_type = m_type

    def ranged_attack(self,all_sprites, direct_attack = None, image = None,
                      dam_mod = 1):
        r_type = None
        image_index = self.r_image_d[self.attack_now_d] + (8 * self.ranged_item)
        if image:            
            r_attack = Ranged(self.attack_d[self.attack_now_d],r_type,
                              self.ranged_attack_group,
                              self.get_pos(),
                              all_sprites,
                              self.ranged_attack_group, direct_attack
                              ,image[image_index],dam_mod)
        else:
            r_attack = Ranged(self.attack_d[self.attack_now_d],r_type,
                              self.ranged_attack_group,
                              self.get_pos(),
                              all_sprites,
                              self.ranged_attack_group, direct_attack, None,
                              dam_mod)
        return self.ranged_attack_group

    def stats_reroll(self):
        self.stats['HP'] += self.mob_type_mod *random.randrange(self.level,self.level*2)
        self.stats['MP'] += self.mob_type_mod * random.randrange(self.level*1,self.level*2)

    def stats_restart(self):
        self.stats['HP'] = self.mob_type_mod *random.randrange(self.level,self.level*2)
        self.stats['MP'] = self.mob_type_mod * random.randrange(self.level*1,self.level*2)
        
    def destroy_mob(self):
        self.kill()
        del self

    def get_ranged_attack_images(self,images):
        self.r_attack_images = images
