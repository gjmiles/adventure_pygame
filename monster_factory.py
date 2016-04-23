from monster import Monster
import random
import pygame
import glob

#A monster generation and handling class
#This makes lots of monsters for each area and handles their attributes
class Monster_Factory():
    def __init__(self,area,collidables,pix_size,screen_size,all_sprites,player,
                 attack_images = None):
        self.area_mobs = area
        self.colids = collidables
        self.pix_size = pix_size
        self.screen = screen_size
        self.monsters = pygame.sprite.LayeredDirty()
        self.all_sprite = all_sprites
        self.check_attack = pygame.sprite.Group()
        self.player = player
        self.ranged_attack_list = None

    #Set ranged attack list
    def set_ranged_attack_list(self,in_list):
        self.ranged_attack_list = in_list
        
    #Generate monsters randomly
    def gen_monsters(self,area = '1'):
        self.area = int(area)
        image_files = glob.glob('*.PNG')
        num_monsters = random.randrange(3,5)
        if area:
            area_folder = 'mob_area' + area + '/*PNG'
            image_files = glob.glob(area_folder)

        while(num_monsters):
            rand_x_pos = random.randrange(0,self.screen[0]-100)
            rand_y_pos = random.randrange(0,self.screen[1]-100)
            new_monster = Monster(rand_x_pos,rand_y_pos,image_files,
                                  self.colids,self.pix_size,int(area))
            colid_test = pygame.sprite.spritecollide(new_monster,
                                                     self.colids,
                                                     False)
            if colid_test:
                continue
            else:
                new_monster.get_ranged_attack_images(self.ranged_attack_list)
                new_monster.group_add(self.all_sprite)
                self.monsters.add(new_monster)
                num_monsters -= 1

    #Simple function to test if monster is near a posistion
    #(i.e.) players position. 
    def is_near(self,monst,pos):
        return [int(abs(x - y)) for x,y in zip(monst.get_pos(),pos)]        

    #Check all monsters to see if they can attack the player or not.
    def monsters_attack(self,pos):
        #all_attacks = []
        m_r_attack = pygame.sprite.Group()
        for monst in self.monsters:
            if monst.mob_type == 'P':
                continue
            player_near_check = self.is_near(monst,pos)
            if player_near_check[0] < 100 and player_near_check[1] < 100:
                #print('Monst attack')
                m_r_attack.add(monst.ranged_attack(self.all_sprite,monst.attack_direct(pos),monst.r_attack_images))
                #all_attacks.append(m_r_attack)
        #if all_attacks:
            #return all_attacks
        if m_r_attack:
            return m_r_attack


    #Monsters will use A* to follow the player if they are close enough,
    #Otherwise they will just randomly wander.
    #Random wandering could use some work.
    def monster_group_follow(self,pos):
        for monst in self.monsters:
            if monst.mob_type == 'P':
                continue
            direction = random.randrange(0,4)
            #player_near_check = [int(abs(x - y)) for x,y in zip(monst.get_pos(),pos)]
            player_near_check = self.is_near(monst,pos)
            if(player_near_check[0] < 250 and player_near_check[1] < 250):
                monst.follow_player(pos)
            else:
                if(direction == 1):
                    monst.changespeed(-1,0)
                elif(direction == 2):
                    monst.changespeed(1,0)
                elif(direction == 3):
                    monst.changespeed(0,1)
                else:
                    monst.changespeed(0,-1)

    #Move monsters wrapper function which goes in main loop to check where
    #monster is moving, if it pathfinding and if it is damaged,
    #Also the player checks if he has leveled or not and the hud is updated,
    #if the player levels.
    def move_monsters(self,all_mobs):
        check_hud_udpate = False
        for monst in self.monsters:
            if monst.mob_type == 'P':
                continue
            monst.move(self.colids,all_mobs)
            monst.is_moving(self.pix_size)
            check_hud_update = monst.damaged(self.check_attack,self.player.stats)
            self.player.is_leveled()
            if check_hud_update:
                self.player.re_hud()

    #Since there are more monsters than the player just have the monsters
    #group build the all mobiles group
    def get_mobiles_group(self):
        return self.monsters

    #Setter function for incoming attack group
    def set_check_attack(self,attack):
        self.check_attack = attack

    #Clear all monsters
    def monsters_clear(self):
        for monst in self.monsters:
            if monst.mob_type == 'P':
                continue
            monst.destroy_mob()
