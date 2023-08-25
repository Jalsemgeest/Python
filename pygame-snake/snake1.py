import time
import pygame, random, sys

# Example 1
# Initialize Pygame
pygame.init()

# # Screen dimensions
screen_width = 640
screen_height = 480

# Colors
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

# # Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jake the Snake")

while True:
    pygame.display.update()