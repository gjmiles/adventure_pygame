import random
import pygame

class Item(pygame.sprite.DirtySprite):
    def __init__(self,x_pos,y_pos,image,all_sprite):
        super().__init__()
        self.sprites = all_sprite
        self.image = pygame.image.load(image[random.randint(0,len(image)-1)]).convert()
        self.dirty = 1
        self.image.set_colorkey(pygame.Color(255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def destroy_item(self):
        self.sprites.remove(self)
        self.kill()
        del self

    def group_add(self,group):
        group.add(self)
