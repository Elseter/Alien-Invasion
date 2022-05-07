import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        # Variables from hell that get 'hold to fire' working
        self.first_press = 0
        self.first_fire = True
        self.previous = 10000

        #alien related variables and objects
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    #---------------------------------------------------------------------------------------
    #Events Handling

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

    #---------------------------------------------------------------------------------------
    #Bullets Handling

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
    
    #---------------------------------------------------------------------------------------
    # Aliens Handling

    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # determine how many fit in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens = available_space_x // (2 * alien_width)

        #Determine how many rows fit
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3* alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        #Create Full Fleet
        for row_number in range(number_rows):
            for alien_number in range(number_of_aliens):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """ Drop the entire Fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_aliens(self):
        """ Update the positions of all the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()



    #---------------------------------------------------------------------------------------


    def _update_screen(self):
        """ update images and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self._check_and_draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Constatly running events
            self._check_events()
            self.ship.update(self)
            self._update_bullets()
            self._update_aliens()
            self._update_screen()


if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()