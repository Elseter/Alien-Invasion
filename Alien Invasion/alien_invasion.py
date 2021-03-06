import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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

        #Create an instance to store game statistics 
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

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

        #Make play button
        self.play_button = Button(self, "Play")

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
    
    def _check_play_button(self, mouse_pos):
        """Start a New Game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)

            # Get rid of any remaining aliesn and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

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
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet alien collisions"""
        #Check if Bullets have impacted Aliens
        #If so, get rid of alien and Bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()
    
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

        #Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    #---------------------------------------------------------------------------------------
    #Game Win/Loss Conditions

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Remove aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause in gameplay
            sleep(0.5)
        else:
            self.sb.check_high_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as being hit
                self._ship_hit()
                break


    #---------------------------------------------------------------------------------------


    def _update_screen(self):
        """ update images and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self._check_and_draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        #Draw play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Constatly running events
            self._check_events()
            if self.stats.game_active:
                self.ship.update(self)
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()