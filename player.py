import glob
import pygame
import math
import random
from pygame.locals import *
from mobile import Mobile
from hud import Hud

#Player is a child of the Mobile class which
#implements player specific actions and attributes
class Player(Mobile):
    
    def __init__(self,x,y,image_files,hud):
        super().__init__(x,y,image_files)
        self.level = 1
        self.mob_type = 'P'
        self.mob_type_mod = 5
        self.check_attack = pygame.sprite.Group()
        self.hud = hud
        self.hud.display_player_stats(self.stats)
        self.speed = 10
        self.ranged_item = 6
        self.stats_reroll()
        self.RE_HUD = USEREVENT + 3
        self.level_chart = {1:50,2:100,3:200,4:500,5:1000,6:3000,7:12800,
                            8:25600,9:51200}
        self.gold = 0

    def restart(self):
        self.stats['Exp'] = 0
        self.level = 1
        self.stop()
        self.stats_restart()
        
    def is_leveled(self):
        level_check = self.level_chart[self.level]
        if self.stats['Exp'] >= level_check:
            self.level += 1
            self.stats_reroll()
            self.stats['Level'] = self.level
        
    def damaged(self):
        if self.check_attack:
            d_checks = pygame.sprite.spritecollide(self,self.check_attack,
                                                   dokill = False)
            if d_checks:
                for d_check in d_checks:
                    d_check.kill()
                    self.stats['HP'] = self.stats['HP'] - d_check.r_type_dam_mod()
                    self.hud.display_player_stats(self.stats,True)
                    pygame.time.set_timer(self.RE_HUD,500)
                    if self.stats['HP'] <= 0:
                        return True
        return False
        
    def set_check_attack(self,check_attack):
        self.check_attack = check_attack

    def check_events(self,event):
        if event.type == self.RE_HUD:
            self.re_hud()

    def re_hud(self):
        self.hud.display_player_stats(self.stats)

    def update(self, add_x = None, add_y = None):
        self.dirty = 1
        self.image = self.directions[self.direction]
        self.mask = self.mask_dict[self.direction]
        
        if self.ranged_attack_group:
            self.ranged_attack_group.update(None,None)
            
        if add_x != None and add_y != None:
            self.rect.x -= add_x
            self.rect.y -= add_y
