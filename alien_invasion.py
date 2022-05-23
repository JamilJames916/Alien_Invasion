import sys
import pygame 
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, ai_game):           #Initialize the game, and create game resources.
       
        super()._init_()
        pygame.init() #1
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #2
        self.screen = pygame.display.set_mode((1200, 800), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.bg_color = (230, 230, 230) # Set the background color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()

    def update(self):
        """Move the alien to the right."""
        self.x += self.settings.alien_speed
        self.rect.x = self.x

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
            self._check_events()
            self.aliens.update() #update the positions of all aliens in the fleet.
            self.ship.update()
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
            
            def _check_keydown_events(self, event):
                """Respond to keypresses."""            
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False 
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.event()     
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

    def _update_screen(self):
            # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            self.aliens.draw(self.screen)
        pygame.display.flip()  #6

           

if __name__ == '_main_':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
