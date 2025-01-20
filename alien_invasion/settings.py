class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1100
        self.screen_height = 600
        self.bg_color = (30, 230, 230)

        # Ship settings.
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_speed_factor = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        #Alien settings.
        self.alien_speed_factor = 1.0
        self.fleet_drop_speed = 20
        #fleet directions: positive = right, negative = left
        self.fleet_direction = 1    
        self.alien_points = 50
        
        self.score_scale = 1.5
        
        #how quickly game speeds up
        self.speedup_scale = 1.1
        
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.speedup_scale)        