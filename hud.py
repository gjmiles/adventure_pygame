import pygame

#This module is for displaying the level and player information on the screen.
class Hud(pygame.sprite.DirtySprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.player_fonts = pygame.font.SysFont('Consolas',
                                                20,
                                                False,
                                                False)
        self.image = pygame.Surface([screen.get_width()//2,30])
        self.image.fill(pygame.Color(0,0,0))
        self.dirty = 1
        self.rect = self.image.get_rect()

    def display_player_stats(self,stats,damaged=False):
        self.image.fill(pygame.Color(0,0,0))
        self.dirty = 1
        stats_text = ''
        for k,v in stats.items():
            stats_text += k + ' ' + str(v) + ' '
        if not damaged:
            self.image.blit(self.player_fonts.render(stats_text,
                                                     True,
                                                     pygame.Color(255,255,255))
                             ,(8,8))
        elif damaged:
            self.image.blit(self.player_fonts.render(stats_text,
                                                     True,
                                                     pygame.Color(255,0,0))
                            ,(8,8))


    def update(self, add_x = None, add_y = None):
        self.dirty = 1
                
