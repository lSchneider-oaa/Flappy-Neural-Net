import random
import numpy as np

import random
import numpy as np

class Bird:
    def __init__(self):
        self.y = 300.0
        self.velocity = 0.0
        self.gravity = 1.2
        self.jump_power = -12.0
        self.is_alive = True
        self.score = 0

    def jump(self):
        self.velocity = self.jump_power

    def update(self):
        # Physics: Apply gravity, update position
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Reward for staying alive
        self.score += 1 

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 50
        self.gap_y = random.randint(150, 450) # Center of the hole
        self.gap_size = 150 # How wide the hole is
        self.speed = 5.0

    def update(self):
        self.x -= self.speed

def check_collision(bird, pipe):
    # 1. Did it hit the floor or the ceiling? (Screen is 600px high)
    if bird.y < 0 or bird.y > 600:
        return True
        
    # 2. Is the bird inside the pipe's X-coordinates? (Bird X is fixed at 100)
    bird_x = 100 
    if pipe.x < bird_x + 20 and pipe.x + pipe.width > bird_x:
        # 3. Is the bird outside the safe gap?
        top_pipe_bottom = pipe.gap_y - (pipe.gap_size / 2)
        bottom_pipe_top = pipe.gap_y + (pipe.gap_size / 2)
        
        if bird.y - 10 < top_pipe_bottom or bird.y + 10 > bottom_pipe_top:
            return True # Hit the pipe!
            
    return False