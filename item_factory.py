from items import Item
import random
import pygame
import glob

#Class which handles items.
class Item_Factory():
    def __init__(self,area,collidables,pix_size,screen_size,all_sprites,player):
        self.area_mobs = area
        self.colids = collidables
        self.pix_size = pix_size
        self.screen = screen_size
        self.items = pygame.sprite.LayeredDirty()
        self.all_sprite = all_sprites
        self.check_attack = pygame.sprite.Group()
        self.player = player

    #Remove a item
    def destroy_item(self):
        self.kill()
        del self

    #Randomly place items on map
    def gen_items(self,special,item = None):
        #print("What")
        image_files = glob.glob('items/*.PNG')
        if not special:
            num_items = random.randrange(2,3)
        else:
            num_items = 1
            image_files = glob.glob(item)

        while num_items:
            if not special:
                rand_x_pos = random.randrange(0,self.screen[0])
                rand_y_pos = random.randrange(0,self.screen[1])
            else:
                rand_x_pos = 100
                rand_y_pos = 300
            #print(rand_x_pos,rand_y_pos)
            new_item = Item(rand_x_pos,rand_y_pos,image_files,self.all_sprite)
            colid_test = pygame.sprite.spritecollide(new_item,
                                                     self.colids,
                                                     False)
            if colid_test:
                continue
            else:
                new_item.group_add(self.all_sprite)
                self.items.add(new_item)
                self.all_sprite.change_layer(new_item,3)
                num_items -= 1

    #Right now items can just be picked up by player, so just check
    #for that.
    def is_picked_up(self):
        for item in self.items:
            player_got = pygame.sprite.collide_rect(item,self.player)
            if player_got:
                item.destroy_item()
                return True
        return False
