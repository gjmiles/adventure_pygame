import pygame
from background_loader import Map_Maker
from item_factory import Item_Factory
#from monster_factory import Monster_Factory

#This class is to handle a lot of generic map and area switching functions.
#For example each map is divided into four areas and this class handles
#The swittching between those areas and it also handles switching to new
#areas and resetting the game.
class Map_Handler():
    def __init__(self,screen,all_sprites,collid_list,player,mobiles,m_fact,
                 hud):
        #Adjacency list for graph of areas
        #Not used
        self.screen = screen
        self.area_graph = {}
        self.area = '1'
        self.areas = {'1':"testDraft.json",'2':'ruins.json'}
        self.sprite_sheet = "Spritesheet/roguelikeSheet_magenta.png"
        self.load_map_sprites = Map_Maker(self.areas['1'],
                                          self.sprite_sheet)
        self.load_map_sprites.get_sprite_list(self.sprite_sheet)
        self.player = player
        self.mobiles = mobiles
        self.all_sprites = all_sprites
        self.collid_list = collid_list
        self.absolute = (0,0)
        self.left = True
        self.top = False
        self.loading = True
        self.switching = False
        self.area_switch = self.load_map_sprites.get_area_switch()
        self.shift_x = 0
        self.shift_y = 0
        self.m_fact = m_fact
        self.hud = hud
        self.ranged_attack_list = self.load_map_sprites.get_sprite_list("magic/SpellFXMissiles.PNG",
                                                                        30,1,False)
        self.player.get_ranged_attack_images(self.ranged_attack_list)
        screen_size = (screen.get_width(),screen.get_height())
        self.item_fact = Item_Factory(None,self.collid_list,50,screen_size,
                                      self.all_sprites,self.player)
        self.m_fact.set_ranged_attack_list(self.ranged_attack_list)
        
    #Switch to a new map
    def switch_area(self,to_switch,new_area):
        self.switching = True
        self.all_sprites.empty()
        self.collid_list.empty()
        self.mobiles.empty()
        self.m_fact.monsters_clear()
        self.load_map_sprites.new_map(to_switch,self.sprite_sheet)
        self.build_area()
        self.switching = False
        self.area = new_area
        #For the demo just end the game when you find this scepter
        if self.area == '3':
            scepter = 'Items/Scepter18.PNG'
            self.item_fact.gen_items(True,scepter)
            
    #Build the map
    def build_area(self):
        self.loading = True
        screen_size = (self.screen.get_width(),self.screen.get_height())
        self.load_map_sprites.build_layers()
        self.load_map_sprites.get_collide_tiles()
        self.load_map_sprites.draw_ground_layer(self.screen,
                                                self.shift_x,
                                                self.shift_y,self.all_sprites)
        
        self.load_map_sprites.draw_above_ground_layer(self.screen,
                                                      self.shift_x,
                                                      self.shift_y,self.all_sprites)
            
        self.load_map_sprites.draw_mid_layer(self.screen,
                                             self.shift_x,
                                             self.shift_y,self.all_sprites)
        
        self.load_map_sprites.draw_mid_c_layer(self.screen,
                                               self.shift_x,
                                               self.shift_y,self.all_sprites)
        
    
        self.player.group_add(self.all_sprites)
        self.load_map_sprites.draw_above_ground_layer(self.screen,
                                                      self.shift_x,
                                                      self.shift_y,self.collid_list)
        self.load_map_sprites.draw_mid_c_layer(self.screen,
                                                      self.shift_x,
                                                      self.shift_y,self.collid_list)
        self.all_sprites.add(self.hud)
        self.all_sprites.change_layer(self.hud,5)
        self.load_map_sprites.draw_top_layer(self.screen,
                                             self.shift_x,
                                             self.shift_y,self.all_sprites)
        spawn_point = self.load_map_sprites.get_spawn_point()
        if not self.switching:
            if spawn_point['properties']['left'] == '1':
                self.left = True
            else:
                self.left = False
            if spawn_point['properties']['top'] == '0':
                self.top = False
            else:
                self.top = True
            self.player.rect.x = spawn_point['x'] * 2
            self.player.rect.y = spawn_point['y'] * 2
            self.absolute = (spawn_point['x']*2,spawn_point['y']*2)
        else:
            warped = self.load_map_sprites.get_warp(self.area)
            self.player.rect.x = warped['x'] *2
            self.player.rect.y = warped['y'] *2
            if warped['properties']['left'] == '1':
                self.left = True
            else:
                self.left = False
            if warped['properties']['top'] == '0':
                self.top = False
            else:
                self.top = True
        self.area_switch = self.load_map_sprites.get_area_switch()

    #Change the section of a map since it is divided into four parts
    #Probably would be better to just have a camera follow the player around
    #instead.
    #This is super buggy.
    def map_section_change(self,pos):
        #Upper right corner
        w = self.screen.get_width()
        h = self.screen.get_height()
        #Instead of doing this it would be better just to have
        #the area warps be made into a collidable tile (Rect)
        #This is probably one the buggiest parts of the game.
        for area in self.area_switch:
            if area['properties']['my_left'] == str(self.left) and  area['properties']['my_top'] == str(self.top):
                goal_check = 0
                if self.top:
                    goal_check = [int(abs(x - y)) for x,y in zip(pos,(area['x']*1,area['y']*2))]
                    if goal_check[0] < 20 and goal_check[1] < 20:
                        self.switch_area(area['properties'][self.area],
                                         area['properties']['area_to'])
                elif not self.top and not self.left:
                    goal_check = [int(abs(x - y)) for x,y in zip((pos[0],pos[1]),(area['x']//2,(area['y']*1)-400))]
                    if goal_check[0] < 20 and goal_check[1] < 20:
                        self.switch_area(area['properties'][self.area],
                                         area['properties']['area_to'])

        if self.loading:
            newpos = []
            newpos.append(self.player.rect.x)
            newpos.append(self.player.rect.y)

            if newpos[1] > h and newpos[0] > w:
                self.map_move(0,h)
                self.player.rect.y = self.player.rect.y + 10
                self.player.rect.y = self.player.rect.x + 10
                self.top = False
                self.left = False
                self.loading = False
                return True
            elif newpos[1] > h:
                self.map_move(0,h)
                self.player.rect.y = self.player.rect.y + 10
                self.top = False
                self.loading = False
                return True
            elif newpos[0] > w:
                self.map_move(-1*w,0)
                self.player.rect.x = w - self.player.image.get_width() - 20
                self.left = False
                self.loading = False
                return True
            else:
                self.loading = False
            
        if (self.left and self.top):
            if(pos[1] < 0):
                self.map_move(0,-1*h)
                self.player.rect.y += h - self.player.rect.y - 10
                self.top == False
                return True
            elif(pos[1] > h):
                self.map_move(0,h)
                self.player.rect.y = self.player.image.get_height() + 10
                self.top = False
                self.loading = False
                return True
        #Left corner
        elif self.left and not self.top:
            #move from bottom to top
            if pos[1] < 0:
                self.map_move(0,-1*h)
                self.player.rect.y = self.screen.get_height() - self.player.image.get_height() - 10
                self.top = True
                return True
            #move left to right
            elif pos[0] > w:
                self.map_move(-1*w,
                              0)
                self.player.rect.x = (self.player.image.get_width() + 10)
                self.left = False
                return True
        #Right corner
        elif self.left == False and self.top == False:
            #move right to left
            if(pos[0] < 0):
                self.map_move(1*self.screen.get_width(),
                              0)
                self.player.rect.x += self.screen.get_width() - self.player.rect.x - 10
                self.left = True
                return True
            #move bottom to top
            elif(pos[1] < 0):
                self.map_move(0,
                              -1*h)
                self.player.rect.y = h -self.player.image.get_height() - 10
                self.top = True
                return True
        #Top right
        elif not self.left and self.top:
            if(pos[0] > w):
                self.map_move(1*w,
                              h)
                self.player.rect.x = w - self.player.image.get_width() - 10
                self.left = True
                return True
            #move bottom to top
            elif(pos[1] > h):
                self.map_move(0,
                              h)
                self.player.rect.y = self.player.image.get_height() + 10
                self.top = False
                return True
        self.loading = False
        return False

    #change the x,y of all the rects for each tile.
    def map_move(self,x,y):
        self.screen.fill(pygame.Color(0,0,0))
        self.collid_list.update(x,y)
        self.all_sprites.update(x,y)

    #Getter for item factory
    def get_item_fact(self):
        return self.item_fact

    #Getter for area
    def get_area(self):
        return self.area

    #Restart the game.
    def restart(self):
        self.switching = False
        self.area = '1'
        self.loading = True
        self.all_sprites.empty()
        self.collid_list.empty()
        self.mobiles.empty()
        self.m_fact.monsters_clear()
        self.player.restart()
        self.load_map_sprites.new_map(self.areas['1'],self.sprite_sheet)
        self.build_area()
