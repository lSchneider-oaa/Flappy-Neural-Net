import random
import numpy as np
from brain import NeuralNet

class Bird:
    def __init__(self):
        self.brain = NeuralNet(3,4,1)
        self.y = 300.0
        self.velocity = 0.0
        self.gravity = 1.2
        self.jump_power = -12.0
        self.is_alive = True
        self.score = 0

    def jump(self):
        self.velocity = self.jump_power
    
    def think(self, pipe):
        bird_y = self.y / 600.0
        pipe_dist = (pipe.x - 100) / 600.0
        pipe_gap = pipe.gap_y / 600.0
        output = self.brain.predict([bird_y, pipe_dist, pipe_gap])
        if output[0][0] > 0.5:
            self.jump()

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

def run_headless_evolution():
    POPULATION_SIZE = 100
    GENERATIONS = 100
    
    # 1. Create Generation 0
    birds = [Bird() for _ in range(POPULATION_SIZE)]
    
    for gen in range(GENERATIONS):
        # Reset the environment for the new generation
        pipes = [Pipe(600)] # Start with one pipe
        active_birds = birds.copy()
        frames = 0
        
        # 2. THE PHYSICS LOOP (Run until all birds are dead)
        while len(active_birds) > 0:
            frames += 1
            
            # Spawn new pipes every 100 frames
            if frames % 100 == 0:
                pipes.append(Pipe(600))
                
            # Update pipes and remove ones that went off screen
            for pipe in pipes:
                pipe.update()
            if pipes[0].x < -50:
                pipes.pop(0)
                
            # Update birds
            for bird in active_birds[:]: # Iterate over a copy so we can remove dead ones
                # Find the pipe that is actually in front of the bird
                target_pipe = pipes[0]
                if target_pipe.x + target_pipe.width < 100 and len(pipes) > 1:
                    target_pipe = pipes[1]

                bird.think(target_pipe)
                bird.update()
                
                if check_collision(bird, pipes[0]):
                    bird.is_alive = False
                    active_birds.remove(bird)
                    
            # Stop the generation if they survive for 5000 frames (they basically solved it)
            if frames > 5000:
                print(f"Gen {gen}: SOLVED! Reached 5000 frames.")
                break 
                
        # 3. THE EVOLUTION LOOP
        # Sort all birds by their score (highest to lowest)
        birds.sort(key=lambda x: x.score, reverse=True)
        best_score = birds[0].score
        print(f"Gen {gen} | Best Score: {best_score}")
        
        # Keep the top 10% (The Elites)
        elites = birds[:10]
        
        # Create the next generation
        next_gen = []
        
        # Copy the elites exactly as they are (so we never lose our best brains)
        for elite in elites:
            new_bird = Bird()
            new_bird.brain = elite.brain.clone()
            next_gen.append(new_bird)
            
        # Fill the remaining 90 slots with mutated babies from the elites
        while len(next_gen) < POPULATION_SIZE:
            parent = random.choice(elites) # Pick a random elite
            baby = Bird()
            baby.brain = parent.brain.clone() # Copy its brain
            baby.brain.mutate(mutation_rate=0.1) # Mutate it!
            next_gen.append(baby)
            
        birds = next_gen

if __name__ == "__main__":
    run_headless_evolution()