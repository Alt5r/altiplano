import pygame
import sys
from boid import *
from tools import *
from random import randint
# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Ball with Velocity")

# Colors
WHITE = (0, 0, 0)
BALL_COLOR = (100, 200, 255)

# Ball settings

boids = []
#ball = boid(screen_width//2, screen_height//2, 3, 2, screen_height, screen_width)
ball_radius = 5
#ball_pos = ball.position()  # Start in the center

for i in range(150):
    boids.append(boid(randint(20,1000), randint(20,1000), randint(-2,2), randint(-2,2), screen_height, screen_width))
print(len(boids))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    #legacy ball movement
    #ball_pos[0] += ball_velocity[0]
    #ball_pos[1] += ball_velocity[1]
    # Fill screen with white
    screen.fill(WHITE)
    #boid updater area
    for ball in boids:
        
        ball.behaviour(boids)
        
        ball_pos = ball.getPosition().parseToInt()
        print(ball_pos)
        # Draw ball
        pygame.draw.circle(screen, ball.getColour(), ball_pos, ball_radius)
        
    
    # Refresh screen
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)  # Limit to 60 FPS
