import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """ Overall class to manage game assets and behavoir"""
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # Create screen, set size and color
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 
            pygame.RESIZABLE)
        pygame.display.set_caption("Alien Invasion")

        # Create Ship Object
        self.ship = Ship(self)
        self.bullet_firing = False
        self.bullets = pygame.sprite.Group()

        # Variables from hell that get the hold to fire working
        self.first_press = 0
        self.first_fire = True
        self.previous = 10000

    def _check_events(self):
        """ Respond to keypresses and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Responds to Keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.bullet_firing = True
            self.first_press = pygame.time.get_ticks()
        elif event.key == pygame.K_q:
            """ Create pause/quit menu?"""
            sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.bullet_firing = False

    def _check_and_draw_bullet(self):
        """Checks if keypress is true, then activates the _fire_bullet method"""
        """Then updates all of the bullets in the bullets group"""
        if self.bullet_firing:
            self._fire_bullet()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  

    def _fire_bullet(self):
        """Create a new bullet if delay from previous matches settings"""
        """Then adds it to bullets group """
        now = pygame.time.get_ticks()
        if self.first_fire:
            if (now - self.first_press >= self.settings.bullet_cooldown):
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.previous = pygame.time.get_ticks()
                self.first_fire = False
        else:
            if (now - self.previous >= self.settings.bullet_cooldown):
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.previous = pygame.time.get_ticks()
    
    def _update_bullets(self):
        """ Update the position of bullets and get rid of old ones"""
        self.bullets.update()

        #Get Rid of Bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
     

    def _update_screen(self):
        """ update images and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self._check_and_draw_bullet()
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Constatly running events
            self._check_events()
            self.ship.update(self)
            self._update_bullets()
            self._update_screen()


if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()