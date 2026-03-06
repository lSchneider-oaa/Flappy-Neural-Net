import random
import numpy as np
from brain import NeuralNet
import pygame
import sys

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
                    
            # Stop the generation if they survive for 5000 frames
            if frames > 5000:
                print(f"Gen {gen}: SOLVED! Reached 5000 frames.")
                
                # Sort the active birds, grab the absolute best one, and return its brain!
                active_birds.sort(key=lambda x: x.score, reverse=True)
                return active_birds[0].brain
                
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
    # If we hit generation 100 without solving it, return the best brain of the final generation
    birds.sort(key=lambda x: x.score, reverse=True)
    return birds[0].brain


import pygame
import sys

def play_champion(champion_brain):
    # Initialize Pygame just for the replay
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Headless Champion Replay")
    clock = pygame.time.Clock()

    # Create a single bird and implant the genius brain
    bird = Bird()
    bird.brain = champion_brain
    
    # Start the level exactly like the simulation
    pipes = [Pipe(600)]
    frames = 0
    running = True

    while running:
        frames += 1
        
        # Handle closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- PHYSICS (Exact same as the simulation) ---
        if frames % 100 == 0:
            pipes.append(Pipe(800))

        for pipe in pipes:
            pipe.update()
            
        if pipes[0].x < -50:
            pipes.pop(0)

        # Find the correct pipe to look at
        target_pipe = pipes[0]
        if target_pipe.x + target_pipe.width < 100 and len(pipes) > 1:
            target_pipe = pipes[1]

        # The brain makes a decision!
        bird.think(target_pipe)
        bird.update()

        # Check for death
        if check_collision(bird, target_pipe):
            print(f"The Champion survived for {frames} frames in the visualizer!")
            running = False 

        # --- DRAWING ---
        screen.fill((135, 206, 235)) # Sky blue background

        # Draw the pipes
        for pipe in pipes:
            # We have to draw two boxes: one above the gap, one below the gap
            top_pipe_bottom = pipe.gap_y - (pipe.gap_size / 2)
            bottom_pipe_top = pipe.gap_y + (pipe.gap_size / 2)
            
            # Top Pipe (starts at y=0, goes down to the gap)
            pygame.draw.rect(screen, (34, 139, 34), (pipe.x, 0, pipe.width, top_pipe_bottom))
            
            # Bottom Pipe (starts at the gap, goes down to y=600)
            pygame.draw.rect(screen, (34, 139, 34), (pipe.x, bottom_pipe_top, pipe.width, 600 - bottom_pipe_top))

        # Draw the Bird (a simple yellow circle)
        pygame.draw.circle(screen, (255, 255, 0), (100, int(bird.y)), 15)

        pygame.display.flip()
        clock.tick(60) # Lock the frame rate to 60 FPS so we can actually watch it

    pygame.quit()

if __name__ == "__main__":
    print("Starting Headless Evolution...")
    champion_brain = run_headless_evolution()
    
    print("Evolution complete! Launching visualizer...")
    play_champion(champion_brain)