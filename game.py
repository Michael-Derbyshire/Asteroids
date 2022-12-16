import pygame

from models import Spaceship, Asteroid
from utils import load_sprite, get_random_position, game_end, update_file

# First we need to initialise a class for the game with functions to make asteroids run
class Roids:
    MIN_ASTEROID_DIST = 200 # Ensures player isn't hit upon starting the game
    SCORE_VALUE = 0 # Initialises player score
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1200, 900))      # Sets the dimensions of the pygame window
        self.background = load_sprite("space", False)           # Sets the background using the load_sprite function
        self.clock = pygame.time.Clock()                        # Initialises the clock to keep movement and projectile speed locked
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        
        self.asteroids = []                                             # Asteroid list
        self.missiles = []                                              # Missile list
        self.spaceship = Spaceship((600, 450), self.missiles.append)    # Initialises spawn location of the spaceship
        
        for _ in range(6):                                      # This loop checks that in the 6 Asteroids that are created if they're
            while True:                                         # distance exceeds the minimum distance required - if it does not
                position = get_random_position(self.screen)     # then it restarts generating asteroids.
                if(
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DIST
                ):
                    break
            
            self.asteroids.append(Asteroid(position, self.asteroids.append))
     
    
    # An indefinite loop to let the game run until completion.    
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
     
     
    # Setting up the window for the game to run in        
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids remake")
     
        
    def _handle_input(self):
        # Setting up ways for players to exit the game 
        for event in pygame.event.get():
            # If the X in the top right or Escape is pressed the game closes
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            # Left click to shoot
            elif(
              self.spaceship
              and event.type == pygame.MOUSEBUTTONDOWN 
              and event.button == 1
            ):
                self.spaceship.shoot()
        
        # Setting controls for the spaceship
        is_key_pressed = pygame.key.get_pressed()
        
        # Controls - Turn right is d, Turn left is a, Accelrate is w
        if self.spaceship:
            #  ---------------Rotation----------------- 
            if is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)
            #  --------------Accleration---------------
            if is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate()
    
    
    def _process_game_logic(self): # Any Processes used to make the game function are done here
        for game_object in self._get_game_objects():
            game_object.move(self.screen) # Processes anything moving - Missiles, Player, Asteroids
            
        if self.spaceship:
            for asteroid in self.asteroids:                 # This section checks for the spaceship in the game logic and checks them against
                if asteroid.collides_with(self.spaceship):  # each asteroid in the asteroids list - for the purpose of looking for collisions
                    self.spaceship = None                   # if it collides it removes control.
                    self.message = "Game Over!"
                    update_file(self.SCORE_VALUE)
                    break
         
        for missile in self.missiles[:]:                    #
            for asteroid in self.asteroids[:]:              # 
                if asteroid.collides_with(missile):         # This section checks for missile and asteroid collision - splitting the asteroid
                    self.asteroids.remove(asteroid)         #
                    self.missiles.remove(missile)           #
                    self.SCORE_VALUE += 10
                    asteroid.split()
                    break
        
                
        for missile in self.missiles[:]:                                    #
            if not self.screen.get_rect().collidepoint(missile.position):   # Makes sure missiles don't wrap around the screen
                self.missiles.remove(missile)                               #
    
        if not self.asteroids and self.spaceship:
            self.message = "You won"
            update_file(self.SCORE_VALUE)
    
    # drawing the contents of the window
    def _draw(self):
        # Background
        self.screen.blit(self.background, (0, 0))
        # Game Objects - Asteroids and Ship
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        # Score
        self._score(self.SCORE_VALUE, 1000, 70)
        
        if self.message:
            game_end(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60) # Sets a base speed for missiles to 60 fps to help run on different machines.
        
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.missiles]
        # Returns all the asteroids and the one ship 
        if self.spaceship:
            game_objects.append(self.spaceship)
            
        return game_objects
    
    # Displays Score
    def _score(self ,SCORE_VALUE, x, y):
        score = pygame.font.Font(None, 50)
        score = score.render('Score:' + str(SCORE_VALUE), False, 'Green')
        self.screen.blit(score, (x, y))