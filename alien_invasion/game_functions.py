from time import sleep
import sys
import pygame

from bullet import Bullet
from alien import Alien

'''
    Game_Functions:
        Included in project when cloned from ehmatthes repo. Functions
        included in functionality for game, this file with purpose to 
        minimize absolute scope of alien_invasion.py to simple game run.
        Will later model my own file like this with the functions already
        included in aliens_invasion.py (TODO)
'''
def check_events(game):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        # click 'X'
        if event.type == pygame.QUIT:
            sys.exit()
        # key presses
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game)
        # click button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_play_button(game, mouse_pos)
            
def check_keydown_events(event, game): 
    """Respond to keypresses."""
    # ship moves
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = True
    # fire bullets
    elif event.key == pygame.K_SPACE:
        fire_bullet(game.settings, game.screen, game.ship, game.bullets)
    # quit game by pressing q
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, game):
    """Respond to key releases."""
    # ship stops moving
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = False

def check_play_button(game, mouse_pos):
    """Start new game when play button pressed."""
    button_clicked = game.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not game.game_active:
        pygame.mouse.set_visible(False)
        
        game.stats.reset_stats()
        game.sb.prep_score()
        game.sb.check_high_score()
        game.sb.prep_level()
        game.sb.prep_ships()
        game.game_active = True
        
        reset_screen(game)
        
def reset_screen(game):
    """Helper function to clear screen and reset game."""
    #clear screen
    game.bullets.empty()
    game.aliens.empty()
    
    #reset screen
    if game.game_active:
        create_fleet(game)
        game.ship.center_ship()
        game.sb.prep_score()
    
def create_fleet(game):
    """Create alien fleet and space alien ships one width apart above/below."""
    alien = Alien(game.settings, game.screen)
    alien_width, alien_height = alien.rect.size
    
    current_x, current_y = alien_width, alien_height
    while current_y < (game.settings.screen_height - 4*alien_height):
        while current_x < (game.settings.screen_width - 2*alien_width):
            create_new_alien(game, current_x, current_y)
            current_x += 2*alien_width
        
        current_x = alien_width
        current_y += 2*alien_height

def create_new_alien(game, x_position, y_position):
    """Create new alien, helper function to create_fleet"""
    new_alien = Alien(game.settings, game.screen)
    new_alien.x = x_position
    new_alien.rect.x = x_position
    new_alien.rect.y = y_position
    game.aliens.add(new_alien)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(game):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    game.screen.fill(game.settings.bg_color)
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in game.bullets.sprites():
        bullet.draw_bullet()
    
    game.ship.blitme()
    game.aliens.draw(game.screen)
    
    # show score info
    game.sb.show_score()
    
    # draw button if game inactive
    if not game.game_active:
        game.play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(game):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    game.bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in game.bullets.copy():
        if bullet.rect.bottom <= 0:
            game.bullets.remove(bullet)
            
    check_bullet_collisions(game)
    
def check_bullet_collisions(game):
    """Check to see if bullets make collisions with alien ships."""
    #check for any bullets that have hit aliens
    collisions = pygame.sprite.groupcollide(
        game.bullets, game.aliens, True, True)
    
    #if fleet destroyed, reset and increase level
    if not game.aliens:
        reset_screen(game)
        
        game.stats.level += 1
        game.sb.prep_level()

    if collisions:
        for aliens in collisions.values():
            game.stats.score += game.settings.alien_points * len(aliens)
            
        game.sb.prep_score()
        game.sb.check_high_score()
        
def update_aliens(game):
    """Update alien fleet for edges or hits."""
    check_fleet_edges(game)
    game.aliens.update()
    
    if pygame.sprite.spritecollideany(game.ship, game.aliens):
        ship_hit(game)
        print("Ship hit!!")
        
    check_aliens_bottom(game)
    
def check_fleet_edges(game):
    """Helper function to _update_aliens."""
    for alien in game.aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game)
            break
    
def ship_hit(game):
    """Resets game for new round of aliens."""
    #decrement ships left and update scoreboard
    game.stats.ships_left -= 1
    game.sb.prep_ships()

    if game.stats.ships_left > 0:
        reset_screen(game)            
        game.settings.increase_speed()

        sleep(0.5)     
    else:
        game.game_active = False
        pygame.mouse.set_visible(True)
        
def check_aliens_bottom(game):
    """Checks if aliens hit bottom of screen."""
    for alien in game.aliens.sprites():
        if alien.rect.bottom >= game.settings.screen_height:
            ship_hit(game)
            break

def change_fleet_direction(game):
    """Drop entire fleet and change direction"""
    for alien in game.aliens.sprites():
        alien.rect.y += game.settings.fleet_drop_speed
    game.settings.fleet_direction *= -1