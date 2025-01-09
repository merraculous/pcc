import pygame
from pygame.sprite import Group
from time import sleep
import sys

#import game_functions as gf
#TODO: to include later after minimizing main AlienInvasion class

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
 
'''
    AlienInvasion:
        Main program run for game alienInvasion. 
        TODO:
            - give option for fullscreen
            - adjust fleet size to screen size
            - visuals
            - change scope of alien_invasion.py with game_functions.py
            - documentation
'''
class AlienInvasion:

    # Initialize pygame, settings, stats, and screen object.
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
        
        #create instance of stats
        self.stats = GameStats(self.settings)
        self.game_active = False
        
        self.play_button = Button(self.settings, self.screen, "Play")
        self.sb = Scoreboard(self.settings, self.screen, self.stats)

        self.ship = Ship(self.settings, self.screen)
        
        # Make groups to store bullets and aliens in
        self.bullets = Group()
        self.aliens = Group()
        
        self._create_fleet()


    #continuous processes for game to be played
    def run_game(self):
        # Start the main loop for the game.
        while True:
            
            self._check_events()
            
            if self.game_active:
                
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            
            self._update_screen()

            self.clock.tick(60)

    
    #periodic checks to see what events happen in game
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
            # mouse clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
            
    #updates based on when player clicks keys
    def _check_keydown_events(self, event):
        # ship moves
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # quit game
        elif event.key == pygame.K_q:
            sys.exit()
            
            
    #updates based on when player releases key on keyboard
    def _check_keyup_events(self, event):
        # ship stops moving
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
      
    #start new game when play button pressed
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            pygame.mouse.set_visible(False)
            
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            
            self._reset_screen()
            

    #update screen based on what is happening in game
    def _update_screen(self):
        # Redraw screen during each pass of loop
        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        #show score info
        self.sb.show_score()
        
        #draw button if game inactive
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()
        
    
    #if all bullets not used fire across screen and add to bullet list
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.settings, self.screen, self.ship)
            self.bullets.add(new_bullet)
            
      
    #update bullet location while on screen
    def _update_bullets(self):
        self.bullets.update()
        
        #remove bullets from Group when reach top of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_collisions()
        
        
        
    def _check_bullet_collisions(self):
        #check for any bullets that have hit aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        #if fleet destroyed, reset and increase level
        if not self.aliens:
            self._reset_screen()
            
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                
            self.sb.prep_score()
            self.sb.check_high_score()
            
        

    # Create alien fleet by creating one alien and continuously adding
    #   to fleet across screen. Each alien one alien size apart.
    #   This is why we use 2*alien_width, so there will always be 
    #   double alien_width measurement to compare to so we don't go 
    #   beypnd space alotted.
    def _create_fleet(self):
        alien = Alien(self.settings, self.screen)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 2*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_new_alien(current_x, current_y)
                current_x += 2*alien_width
            
            current_x = alien_width
            current_y += 2*alien_height
        
        
    #Create new alien to add to aliens fleet. Each alien one alien width 
    #   apart.This is why we use 2*alien_width, so there will always be 
    #   double alien_width measurement to compare to so we don't go 
    #   beypnd space alotted.
    def _create_new_alien(self, x_position, y_position):
        new_alien = Alien(self.settings, self.screen)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    
    #Check if fleet is at an edge and update position.
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Ship hit!!")
            
        self._check_aliens_bottom()
        
    
    #Helper function to _update_aliens.
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
            
    #Drop entire fleet and change direction
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
        
    #resets game for new round of aliens
    def _ship_hit(self):
        #decrement ships left and update scoreboard
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        
        if self.stats.ships_left > 0:
            self._reset_screen()            
            self.settings.increase_speed()
    
            sleep(0.5)     
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

        
    #checks if aliens hit bottom of screen
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    
    #helper function for clear screen and reset game
    def _reset_screen(self):
        #clear screen
        self.bullets.empty()
        self.aliens.empty()
        
        #reset game
        if self.game_active:
            self._create_fleet()
            self.ship.center_ship()
       
        
if __name__ == '__main__':
    #make game instance and run game.
    ai = AlienInvasion()
    ai.run_game()
