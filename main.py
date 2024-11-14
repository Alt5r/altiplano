import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Ball with Velocity")

# Colors
WHITE = (0, 0, 0)
BALL_COLOR = (100, 200, 255)

# Ball settings
ball_radius = 10
ball_pos = [screen_width // 2, screen_height // 2]  # Start in the center
ball_velocity = [3, 2]  # [x_velocity, y_velocity]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Handle screen boundaries (bounce off edges)
    if ball_pos[0] <= ball_radius or ball_pos[0] >= screen_width - ball_radius:
        ball_velocity[0] = -ball_velocity[0]
    if ball_pos[1] <= ball_radius or ball_pos[1] >= screen_height - ball_radius:
        ball_velocity[1] = -ball_velocity[1]

    # Fill screen with white
    screen.fill(WHITE)

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, ball_radius)

    # Refresh screen
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)  # Limit to 60 FPS
