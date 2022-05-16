class Settings:
    """ A class to store all the settings for Alien Invasion"""

    def __init__(self):
        """ Initialize the game's settings"""

#---------------------------------------------------------------------------------------
# Windows 2056x1080 Settings (active by default)

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship Settings
        self.ship_speed = 1.0     # default = 1.0 (Mac = 7.0)
        self.ship_limit = 3


        #Bullet Settings
        self.bullet_speed = 1.0      # default = 1.0 (Mac = 10)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_cooldown = 300     # default 300 (Mac = 500)

        #Alien settings
        self.alien_speed = 0.2         # default = 0.2 (Mac = 1)
        self.fleet_drop_speed = 5      # default = 5 (Mac = 5)
        self. fleet_direction = 1      # 1 = Right, -1 = left
