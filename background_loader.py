#!/usr/bin/python3

#tmx files are xml files so from the python 3.4 documentation I used:
#https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
#This way I can retrieve object information to easily integrate
#collision detection between tiled maps and my game engine.

#I actually ended up using json because json files are just
#python dictionaries and lists.  I still kept the xml stuff in case.
import xml.etree.ElementTree as ET
import json
import pygame

#class Tile(pygame.sprite.Sprite):
#A class to handle each individual tile.
class Tile(pygame.sprite.DirtySprite):
    def __init__(self,image_in,layer,item = False):
        super().__init__()

        self.image = image_in
        self.image = pygame.transform.scale(self.image, (32,32))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.dirty = 1
        self.layer = layer
        self.item = item

    def update(self, add_x = None, add_y = None):
        if add_x != None and add_y != None:
            self.dirty = 1
            self.rect.x += add_x
            self.rect.y -= add_y

    def destroy(self):
        self.kill()
        del self
        
#A class to make the map and get sprites from a spritesheet.
#handles both tiled json files and sprite sheets as long as the
#sprite sheet is neatly formatted (a square or rectangular sprite,
#and a fixed distance between each sprites) would need more modifications,
#if things were formatted differently.
class Map_Maker():
    def __init__(self,filename,sprite_sheet):
        self.filename = filename
        self.spritesheet = sprite_sheet
        self.ground_layer = []
        self.above_ground = []
        self.top_layer = []
        self.mid_layer = []
        self.mid_c_layer = []
        self.tiles = []
        self.collide_tiles = []
        self.removable_tiles = []
        self.spawn_point = {}
        self.area_switch = []
        self.item_tile = []
        # tree = ET.parse(filename)
        # self.root = tree.getroot()
        # self.tileProperties = []
        # self.layers = []

    #Reset and add a new map from a different json file.
    def new_map(self,filename,sprite_sheet):
        self.ground_layer = []
        self.above_ground = []
        self.top_layer = []
        self.collide_tiles = []
        self.removable_tiles = []
        self.spawn_point = {}
        self.area_switch = []
        self.filename = filename
        self.spritesheet = sprite_sheet
        self.tiles.clear()
        self.get_sprite_list(self.spritesheet)            

    def get_area_switch(self):
        return self.area_switch

    def get_all_dicts(self):
        interactObject =[]
        for objectInfo in root.iter('object'):
            interactObject.append(objectInfo.attrib)

        return interactObject

    def get_spawn_point(self):
        # spawnPoint = {}
        
        # for objectInfo in root.iter('object'):
        #     if(objectInfo.attrib['name'] == 'SpawnPoint'):
        #         spawnPoint = objectInfo.attrib
        #         interactObject.append(objectInfo.attrib)

        return self.spawn_point

    def json_load_file(self):
        f = open(self.filename)
        entry = json.load(f)
        self.layers = entry['layers']
        self.tileProperties = entry['tilesets'][0]['tileproperties']
        
    #This gets the layers from the tiled json file
    def build_layers(self):
        self.json_load_file()
        #Get tiles with properties]
        #Get different layers
        #Build a group of images
        for layer in self.layers:
            if(layer['name'] == 'topLayer'):
                self.top_layer = layer
            elif(layer['name'] == 'midLayer'):
                 self.mid_layer = layer
            elif(layer['name'] == 'midLayerCollide'):
                self.mid_c_layer = layer
            elif(layer['name'] == 'AboveGround'):
                self.above_ground = layer
            elif(layer['name'] == 'GroundLayer'):
                self.ground_layer = layer
            elif(layer['name'] == 'Object Layer 1'):
                for x in layer['objects']:
                    if x['name'] == 'SpawnPoint':
                        self.spawn_point = x
                    if x['name'] == 'AreaSwitch':
                        self.area_switch.append(x)
                        
    #Gets the area of the map which is supposed to move to another area.
    def get_warp(self,from_area):
        for layer in self.layers:
            if layer['name'] == 'Object Layer 1':
                for x in layer['objects']:
                    if x['name'] == from_area:
                        return x
                    
    #This gets the collision tiles and could get other tile attributes also.
    def get_collide_tiles(self):
        for k in self.tileProperties:
            self.collide_tiles.append(k)
        for check in self.collide_tiles:
            if('Remove' in self.tileProperties[check]):
                self.removable_tiles.append(check)
            if 'Gold' in self.tileProperties[check]:
                self.item_tile.append(check)
                
        return self.collide_tiles

    #Wrapper functions for each layer
    def draw_mid_layer(self,screen,shift_x,shift_y,group):
        self.draw_layer(self.mid_layer,screen,shift_x,shift_y,group,1)

    def draw_mid_c_layer(self,screen,shift_x,shift_y,group):
        self.draw_layer(self.mid_c_layer,screen,shift_x,shift_y,group,3)
        
    def draw_ground_layer(self,screen,shift_x,shift_y,group):
        self.draw_layer(self.ground_layer,screen,shift_x,shift_y,group,0)

    def draw_above_ground_layer(self,screen,shift_x,shift_y,group):
        self.draw_layer(self.above_ground,screen,shift_x,shift_y,group,0)

    def draw_top_layer(self,screen,shift_x,shift_y,group):
        self.draw_layer(self.top_layer,screen,shift_x,shift_y,group,4)

    #Draws the layer based on its wrapper layers properties
    def draw_layer(self,layer,screen,shift_x,shift_y,group,layer_sprite):
        draw_x = 0 
        draw_y = 0 
        if(draw_y > layer['height']):
            draw_y = layer['height']
        if(draw_x > layer['width']):
            draw_x = layer['width']

        x_index = 0
        y_index = 0
        tile_test = Tile(self.tiles[0],layer_sprite)
        tile_width = tile_test.image.get_width()
        tile_height = tile_test.image.get_height()
        for index,tile in enumerate(layer['data']):
            if(tile - 1 == -1):
                x_index+=1
                draw_x+= tile_width
                if(layer['width'] == x_index):
                    x_index = 0
                    draw_x = 0
                    draw_y+= tile_height
                continue

            if self.item_tile.count(str(tile-1)):
                new_tile = Tile(self.tiles[tile-1],layer_sprite,True)
            else:
                new_tile = Tile(self.tiles[tile-1],layer_sprite)
            new_tile.rect.x = draw_x - shift_x
            new_tile.rect.y = draw_y - shift_y
            group.add(new_tile)
            group.change_layer(new_tile,layer_sprite)
            x_index+=1
            draw_x+=tile_width
            if(layer['width'] == x_index):
                x_index = 0
                draw_x = 0
                draw_y+=tile_height
                
    #This handles getting the sprites out of a spritesheet and into
    #a pygame sprite group.
    def get_sprite_list(self,sprite_sheet,size = 16, offset = 1,load_tiles = True):
        sprite_list = []
        total_surface = pygame.image.load(sprite_sheet).convert()

        sheet_width = total_surface.get_width()
        sheet_height = total_surface.get_height()
        current_x = 0
        current_y = 0
        while(sheet_height > current_y):
            while(sheet_width > current_x):
                image = pygame.Surface([size,size,]).convert()
                image.blit(total_surface,(0,0),(current_x,current_y,size,size))
                image.set_colorkey(pygame.Color(255,0,255))
                sprite_list.append(image)
                current_x += (size + offset)
            current_x = 0
            current_y += (size + offset)
        if load_tiles:
            self.tiles = sprite_list
        return sprite_list
