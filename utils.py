import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2

# Loads sprites from the assets folder when called
def load_sprite(name, with_alpha=True):
    path = f"Asteroids/assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha: # Fiuxes any broken sprites alpha values
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()
    

# Wraps any objects around the screen to make sure they don't leave the screen.
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w , y % h)

# Generate random coordinates on the screen for the asteroids to spawn in
def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )
    
# Generate random velocity for the asteroids
def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)    # Sets a random speed between the minimum and max passed into the method
    angle = random.randrange(0, 360)                 # Sets a random angle between the range 0-360
    return Vector2(speed, 0).rotate(angle)

# Displays the Game Over screen
def game_end(surface, text, font, color = Color("tomato")):
    text_surface = font.render(text, True, color)
    
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)

# Updates a tile to keep track of scores - can be used to have a scoreboard in the future
def update_file(x):
    with open(r"Asteroids/Asteroids-Game/scores.txt", 'a') as file:
        line = str(x)
        file.write(line + "\n")