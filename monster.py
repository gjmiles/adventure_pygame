import pygame
import math
from mobile import Mobile
from pathfinding import a_star

#This is a child of the mobile class and is responsible for
#handling attributes and functions which are specific to an
#individual monster.
class Monster(Mobile):
    
    def __init__(self,x,y,image_files,collid_list,pix_size,area = 1):
        super().__init__(x,y,image_files)
        
        self.pix_size = pix_size
        self.path_finder = a_star(collid_list,pix_size)
        self.mob_type = 'M'
        self.exp = self.level*10 * area
        self.level = area * 2
        self.stats_reroll()

    def follow_player(self,pos):
        self.follow_path(self.path_finder.get_path(self.get_pos(),pos),
                         self.pix_size,
                         pos)

    #see if monster is hurt and if dead or not.
    def damaged(self,attack_group,stats):
        if attack_group:
            d_check = pygame.sprite.spritecollideany(self,attack_group)
            if d_check:
                d_check.kill()
                self.stats['HP'] = self.stats['HP'] - d_check.r_type_dam_mod()
                if self.stats['HP'] <= 0:
                    stats['Exp'] += self.exp
                    self.destroy_mob()
                    return True
        return False

    def attack_direct(self,player_pos):
        #monster has to attack in players direction
        #monster is just going to shoot right at player
        #uses a unit vector

        x_dx = player_pos[0] - self.rect.x
        y_dx = player_pos[1] - self.rect.y

        len_v = math.sqrt(abs(x_dx)**2 + abs(y_dx)**2)

        if(not x_dx//len_v or not y_dx//len_v):
            return (math.ceil(x_dx/len_v),math.ceil(y_dx/len_v))
        else:
            return (x_dx//len_v,y_dx//len_v)
