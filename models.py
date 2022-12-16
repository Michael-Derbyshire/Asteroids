from pygame.math import Vector2 
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sprite, wrap_position

class GameObject:
    def __init__(self, position, sprite, velocity): # Initialising Super class of Game object which all classes in this game will inherit from due to simple and fully used attributes.
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width()/2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface): # Draws the object at it's position vector with the centre of the sprite on the Vector2 Value.
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
        
    def move(self, surface): # Moves the object in the direction of the velocity placed upon the object
        self.position = wrap_position(self.position + self.velocity, surface)
        
    def collides_with(self, other_object): # Checks if the current object has collided with another object and returns the value if it does - the value is checked via the object radius.
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius
    
UP = Vector2(0, -1) # A reference to the natural "UP" value of pygame.

class Spaceship(GameObject): # Spaceship subclass
    rotationPotential = 3
    acceleration = 0.3
    missileSpeed = 5

    def __init__(self, position, create_missile_callback):
        self.create_missile_callback = create_missile_callback # The callback will add the missile to the missile list
        # Make a copy of the original "UP" Vector
        self.direction = Vector2(UP)        

        super().__init__(position, load_sprite("Spaceship"), Vector2(0)) # Initialises the object with the "Spaceship.png" sprite and sets velocity to 0
        
    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1 # Flips direction between clockwise and anticlockwise
        angle = self.rotationPotential * sign # Updates the angle value
        self.direction.rotate_ip(angle) # Updates the direction of the ship based on the angle calculated.
        
    def accelerate(self): # Moves the player forward upon a button being pressed.     
        self.velocity += self.direction * self.acceleration   
        
    def shoot(self): # Fires missiles
        missile_velocity = self.direction * self.missileSpeed + self.velocity # Makes sure the bullet is always quicker than the player
        missile = Missile(self.position, missile_velocity)
        self.create_missile_callback(missile) # Sends the missile to the players list 
        
        
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0) # Rotozoom is a function from pygames responsible for two things - Rotating and Scaling Images
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        
class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size = 3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        
        size_to_scale = {   #
            3: 1,           # I found this online to figure out how to scale down the asteroids upon splitting
            2: 0.5,         # I do not fully understand how it worsk with rotozoom yet.
            1: 0.25,        #
        }
        
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("Asteroid"), 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3)) # Initialisation for Asteroids
    
    # Splits the asteroid into smaller sub-asteroids upon collision with missiles.
    def split(self): 
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size -1
                )
                self.create_asteroid_callback(asteroid)
        
class Missile(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("Missile"), velocity)
        
    def move(self, surface):
        self.position = self.position + self.velocity