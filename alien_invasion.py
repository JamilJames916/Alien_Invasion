import sys
import py
import pygame 
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):           #Initialize the game, and create game resources.
       
        pygame.init() #1
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #2
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.bg_color = (230, 230, 230) # Set the background color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
                                        #Start the main loop for the game.
        while True:                        #3
            #Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self.bullets.update()
            #get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))

            self._update_screen()
    
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
        pygame.display.flip()  #6

           

if __name__ == '_main_':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
