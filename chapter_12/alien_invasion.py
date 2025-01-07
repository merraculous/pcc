import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf

import sys

class AlienInvasion:

    # Initialize pygame, settings, and screen object.
    #   Note: PCC show how to make game window fullscreen. On my own 
    #   system, did not work well or better so for this project, 
    #   window will remain defined in settings.py
    #       -may return to later
    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self.settings, self.screen)
        
    

    def run_game(self):
        '''       
        # Make a group to store bullets in.
        bullets = Group()
        '''

        # Start the main loop for the game.
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

            self.clock.tick(60)
            
            
            '''
            gf.check_events(ai_settings, self.screen, ship, bullets)
            ship.update()
            gf.update_bullets(bullets)
            gf.update_screen(ai_settings, self.screen, ship, bullets)
            '''
            
    def _check_events(self):
    
        # respond to key events or mouse presses.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # if a key is pressed
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                    
            # if a key is released
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
                    
    def _check_keydown_events(self, event):
        
        # ship moves
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            
        elif event.key == pygame.K_q:
            sys.exit()
            
            
    def _check_keyup_events(self, event):
        
        # ship stops moving
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
            
    def _update_screen(self):
        
        # Redraw screen during each pass of loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        pygame.display.flip()


if __name__ == '__main__':
    #make game instance and run game.
    ai = AlienInvasion()
    ai.run_game()
