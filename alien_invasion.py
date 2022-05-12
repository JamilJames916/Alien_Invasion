import sys
import pygame 
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):           #Initialize the game, and create game resources.
       
        pygame.init() #1
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #2
        pygame.display.set_caption("Alien Invasion")

        self.bg_color = (230, 230, 230) # Set the background color
        self.ship = Ship(self)

    def run_game(self):
                                        #Start the main loop for the game.
        while True:                        #3
            #Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self._update_screen()
    
    def _check_events(self):
            for event in pygame.event.get():   #4
                if event.type == pygame.QUIT:  #5
                   sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                         self.ship.moving_right = True    # move the ship to the right.
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False       
                        self.ship.rect.x += 1

    
    def _update_screen(self):
            # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
            # Make the most recently draw screen visible.
        pygame.display.flip()  #6

           

if __name__ == '_main_':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
