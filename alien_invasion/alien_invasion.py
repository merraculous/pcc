import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
 
'''
    AlienInvasion:
        Main program run for game alienInvasion. 
        TODO/kinda optional:
            - give option for fullscreen
            - visuals
            - documentation
'''
class AlienInvasion:

    def __init__(self):
        """Initialize game, settings, stats, and screen object."""
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        #create instance of stats
        self.stats = GameStats(self.settings)
        self.game_active = False
        
        self.play_button = Button(self.settings, self.screen, "Play")
        self.sb = Scoreboard(self.settings, self.screen, self.stats)

        self.ship = Ship(self.settings, self.screen)
        
        # Make groups to store bullets and aliens in
        self.bullets = Group()
        self.aliens = Group()
        
        gf.create_fleet(self)

    def run_game(self):
        """Continuous game play."""
        # Start the main loop for the game.
        while True:
            gf.check_events(self)
            
            if self.game_active:
                self.ship.update()               
                gf.update_bullets(self)
                gf.update_aliens(self)
                
            gf.update_screen(self)
            self.clock.tick(60)
     
if __name__ == '__main__':
    #make game instance and run game.
    ai = AlienInvasion()
    ai.run_game()
