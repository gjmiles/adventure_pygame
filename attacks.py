import random
import pygame

#This module is all the attacks, for the class demo just a ranged attack
#This handles all the attributes for an attack and its sprite and how
#much damage it does and how far it goes
class Ranged(pygame.sprite.DirtySprite):
    def __init__(self,direct,r_type,sprites,mob_pos,all_sprites,ranged_group,
                 direct_to = None, image = None,dam_mod = 1):
        super().__init__()

        if not image:
            self.image = pygame.Surface([2, 5])
            self.image.fill(pygame.Color(0, 0, 0))
        else:
            self.image = image

        self.rect = self.image.get_rect()

        #Types will be a dict containing all the different types of weapons.
        #Probbly would use an xml or other file if this was more than just a prototype.
        types = {}
        self.r_type = r_type
        self.direct = direct
        self.dist = self.r_type_dist_mod()
        self.sprites = all_sprites
        self.mob_pos = mob_pos
        self.rect.x = mob_pos[0]
        self.rect.y = mob_pos[1]
        self.dirty = 1
        self.layer = 2
        self.ranged_group = ranged_group
        self.direct_to = direct_to
        ranged_group.add(self)
        all_sprites.add(self)
        all_sprites.change_layer(self,2)
        self.dam_mod = dam_mod
        #print(all_sprites.get_layer_of_sprite(self))

    def clear_surface(self):
        self.image = None

    def update(self,add_x = None, add_y = None):
        self.dirty = 1
        #print(self.direct)
        if self.direct_to != None:
            #print(self.direct_to)
            self.rect.x += self.direct_to[0] * self.r_type_speed_mod()
            self.rect.y += self.direct_to[1] * self.r_type_speed_mod()
        else:
            self.rect.x += self.direct[0] * self.r_type_speed_mod()
            self.rect.y += self.direct[1] * self.r_type_speed_mod()
        self.dist -= 1
        if not self.dist:
            self.sprites.remove(self)
            self.ranged_group.remove(self)
            
    def r_type_dist_mod(self):
        return random.randrange(15,20)

    def r_type_speed_mod(self):
        return 5

    def r_type_dam_mod(self):
        return random.randrange(2*self.dam_mod,3*self.dam_mod)
