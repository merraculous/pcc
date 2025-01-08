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
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        #Alien settings.
        self.alien_speed_factor = 1.0
        self.fleet_drop_speed = 100
        #fleet directions: 1 = right, -1 = left
        self.fleet_direction = 1        
        