import sys
import os
import platform
import py
import pygame 
from time import sleep
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, ai_game):           #Initialize the game, and create game resources.
       
        super()._init_()
        pygame.init() #1
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #2
        self.screen = pygame.display.set_mode((1200, 800))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = GameStats(self)

        self.bg_color = (230, 230, 230) # Set the background color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()

        # Make the Play Button.
        self.play_button = Button(self, "Play")

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
        # Decrement ships_left. 
            self.stats.ships_left -= 1

            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen>
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #Make an alien.
        #Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of alien that fit on the screen. 
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height)- ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):


        #Create the first row of aliens.
            for row_number in range(number_rows):
             for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
                                        #Start the main loop for the game.
        while True:                        #3
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
            self._check_events()
            if self.stats.game_active:
                self.aliens.update() #update the positions of all aliens in the fleet.
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
            self._update_aliens()
            self._update_screen()
            #get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))

           
    
    def _check_events(self):
            for event in pygame.event.get():   #4
                if event.type == pygame.QUIT:  #5
                   sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                    if event.key == pygame.K_RIGHT:
                         self.ship.moving_right = True    # move the ship to the right.
                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = True
                        
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

            def _check_play_button(self, mouse_pos):
                """Start a new game when the player clicks Play."""
                button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                if button_clicked and not self.stats.game_active:
                    pygame.mouse.set_visible(False)
                if self.play_button.rect.collidepoint(mouse_pos):
                    self.stats. reset_stats()
                    self.stats.game_active = True
                # Get rid of any remaining aliens and bullets.
                    self.aliens.empty()
                    self.bullets.empty()
                    # Create a new fleet and center the ship.
                    self._create_fleet()
                    self.ship.center_ship()

            def _check_keydown_events(self, event):
                """Respond to keypresses."""            
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False 
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.exit()     
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                    self.ship.rect.x += 1
            
            def _fire_bullet(self):
                """Create a new bullet and add it to the bullets group."""
                if len(self.bullets) < self.settings.bullets_allowed:
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided. 

    def _update_screen(self):
            # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            self.aliens.draw(self.screen)
        # Draw the play button if the game is inactive. 
            if not self.stats.game_active:
                self.play_button.draw_button()
        pygame.display.flip()  #6

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._changes_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit. 
                self._ship_hit()
                break

           

if __name__ == '_main_':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
