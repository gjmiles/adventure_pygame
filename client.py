#!/usr/bin/python3

#This is the main module that is also used to start the game.

import pygame
import time
import glob
from mobile import Mobile
from background_loader import Map_Maker
from pathfinding import a_star
from monster import Monster
from player import Player
from monster_factory import Monster_Factory
from pygame.locals import *
from hud import Hud
from map_handler import Map_Handler
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT =800

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Dungeon Dreams Demo")
 
    # Create the player
    map_pix_size = 30

 
    # Create all the levels
    level_list = []
#    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = 0
#    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()

 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    all_sprites_list = pygame.sprite.LayeredDirty()
    collid_list = pygame.sprite.LayeredDirty()
    mobiles_list = pygame.sprite.Group()
    m_attacks = pygame.sprite.Group()
    area = None
    image_files = glob.glob('HumanMage.PNG')
    hud = Hud(screen)
    player = Player(100,100,image_files,hud)
    hud.display_player_stats(player.stats)
    player.set_all_sprites(all_sprites_list)
    screen_size = (screen.get_width(),screen.get_height())
    m_fact = Monster_Factory(area,collid_list,50,screen_size,all_sprites_list,player)
    map_tool = Map_Handler(screen,all_sprites_list,collid_list,player,mobiles_list,
                           m_fact,hud)
    map_tool.build_area()
    item_fact = map_tool.get_item_fact()

    shift_x = 0
    shift_y = 0
    
    all_mobiles = m_fact.get_mobiles_group()
    dam_mod = 1
    #init path finding...
    path_finder = a_star(collid_list,50)
    player.group_add(all_mobiles)

    image_files = glob.glob('*.PNG')
    
    #init events for following and monsters, start at 3 seconds because
    #player needs a second or two catch bearings
    FOLLOW_EVENT = USEREVENT + 1
    M_ATTACK_EVENT = USEREVENT + 2
    pygame.time.set_timer(FOLLOW_EVENT, 3000)
    pygame.time.set_timer(M_ATTACK_EVENT,3000)
    game_start = False
    #-------- Main Program Loop -----------
    while not done:

        #Probably would make a class just to handle
        #client events.
        #These handle the movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            player.changespeed(-1, 0)
        if keys[pygame.K_l]:
            player.changespeed(1, 0)
        if keys[pygame.K_k]:
            player.changespeed(0, -1)
        if keys[pygame.K_j]:
            player.changespeed(0, 1)
        if keys[pygame.K_n]: 
            player.changespeed(1,1)
        if keys[pygame.K_b]: 
            player.changespeed(-1,1)
        if keys[pygame.K_y]:
            player.changespeed(-1,-1)
        if keys[pygame.K_u]:
            player.changespeed(1,-1)

        #More events, quit and attacks and stopping the player
        #when the button goes up.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            player.check_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    r_attack = player.ranged_attack(all_sprites_list,
                                                    None,
                                                    player.r_attack_images,
                                                    dam_mod)
                    m_fact.set_check_attack(r_attack)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    player.stop()
                if event.key == pygame.K_y:
                    player.stop()
                if event.key == pygame.K_k:
                    player.stop()
                if event.key == pygame.K_u:
                    player.stop()
                if event.key == pygame.K_l:
                    player.stop()
                if event.key == pygame.K_n:
                    player.stop()
                if event.key == pygame.K_j:
                    player.stop()
                if event.key == pygame.K_b:
                    player.stop()

            #Really for testing pathfinding, pathfinding is really for monsters.
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                player.follow_path(path_finder.get_path(player.get_pos(),pos),
                                   map_pix_size,
                                   pos)

            #Monsters follow every two seconds to cut down on pathfinding
            #Calculations
            if event.type == FOLLOW_EVENT:
                m_fact.monster_group_follow(player.get_pos())
                pygame.time.set_timer(FOLLOW_EVENT, 2000)

            #Attack every second which is kind of a lot still
            #Otherwise player would get hurt too fast or too slow.
            if event.type == M_ATTACK_EVENT:
                m_attacks = m_fact.monsters_attack(player.get_pos())
                player.set_check_attack(m_attacks)
                pygame.time.set_timer(M_ATTACK_EVENT,1000)

        #Move the player and then check for game end or picked up item.
        player_pos = player.move(collid_list,all_mobiles)
        lost = player.damaged()
        m_fact.move_monsters(all_mobiles)
        got_item = item_fact.is_picked_up()
        #For now just one item and if it is picked up the player wins.
        if got_item:
            end_text = []
            end_text.append('You Found the Scepter of Yendor and Won the Game!')
            end_text.append('To replay press r!')
            end_text.append('To quit press q!')
            end_text.append('To continue press Space Bar!')
            done = game_end(True,end_text,screen,map_tool)
            map_tool.map_move(0,0)
            player.stop()
            player.ranged_item = 3
            player.speed = 8
            player.dam_mod = 10
        elif(lost):
            end_text = []
            end_text.append('You perished!')
            end_text.append('To replay press r!')
            end_text.append('To quit press q!')
            done = game_end(False,end_text,screen,map_tool)
            
        if(map_tool.map_section_change(player_pos)):
            area = map_tool.get_area()
            m_fact.gen_monsters(area)
        
        player.is_moving(map_pix_size)
        all_mobiles.update(None,None)
        if m_attacks:
            m_attacks.update()
        all_sprites_list.draw(screen)
        
        clock.tick(25)
        pygame.display.flip()
        
    pygame.quit()
 

#Function to handle game end, would probably go in an event handling class.
def game_end(won,end_text,screen,map_tool):
    replay = True
    fonts = pygame.font.SysFont('kenpixel_square.ttf',
                                30,
                                False,
                                False)
    #Just to get the font y size.
    font_size = fonts.size('sample')
    end_image = pygame.Surface([screen.get_width()-100,
                                screen.get_height()-100])
    while replay:
        screen.fill(pygame.Color(0,0,0))
        y_rend_pos = 200
        for t in end_text:
            screen.blit(fonts.render(t,
                                     False,
                                     pygame.Color(255,0,255))
                        ,(200,y_rend_pos))
            y_rend_pos += font_size[1]
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and won:
                    replay = False
                if event.key == pygame.K_r:
                    replay = False
                    map_tool.restart()
                if event.key == pygame.K_q:
                    replay = False
                    return True
    return False

if __name__ == "__main__":
    main()
