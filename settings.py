class Settings:
    """store all settings in the game"""

    def __init__(self):
        """initialize game settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (70,140,50)
        self.ship_upper_boundary = 800
        self.ship_limit = 3
        self.bullet_width = 6
        self.bullet_height = 30
        self.bullet_color = (230,0,0)
        self.bullets_allowed = 3
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 4.0
        self.bullet_speed = 5.5
        self.alien_speed = 1.0
        # when fleet_direction is 1, moving right; when it's -1, moving left
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
